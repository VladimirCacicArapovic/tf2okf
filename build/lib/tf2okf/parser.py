from __future__ import annotations

import json
import re
import shutil
import subprocess
from pathlib import Path
from typing import Any

from .model import IamPolicyFact, IamStatement, Module, Output, Provider, Resource, TerraformModel, Variable
from .security import MAX_SUBPROCESS_OUTPUT, should_read

BLOCK_RE = re.compile(r'(?m)^\s*(resource|data|module|variable|output|provider)\s+"([^"]+)"(?:\s+"([^"]+)")?\s*\{')
REF_RE = re.compile(
    r"\b(?:data\.)?[A-Za-z_][\w-]*\.[A-Za-z_][\w-]*(?:\.[A-Za-z_][\w-]*)?|\bmodule\.[A-Za-z_][\w-]*|\bvar\.[A-Za-z_][\w-]*|\blocal\.[A-Za-z_][\w-]*"
)
ATTR_RE = re.compile(r"(?m)^\s*([A-Za-z_][\w-]*)\s*=\s*(.+?)\s*$")
_POLICY_REF_RE = re.compile(r"\b(?:data\.)?aws_iam_policy_document\.[A-Za-z_][\w-]*\.(json|rendered)\b")
_ATTACHMENT_TARGETS = {
    "aws_iam_group_policy_attachment": "group",
    "aws_iam_role_policy_attachment": "role",
    "aws_iam_user_policy_attachment": "user",
}


def _balanced_block(text: str, open_pos: int) -> tuple[str, int]:
    depth, i = 0, open_pos
    in_str = False
    escape = False
    line_comment = False
    block_comment = False
    while i < len(text):
        c = text[i]
        n = text[i + 1] if i + 1 < len(text) else ""
        if line_comment:
            if c == "\n":
                line_comment = False
            i += 1
            continue
        if block_comment:
            if c == "*" and n == "/":
                block_comment = False
                i += 2
                continue
            i += 1
            continue
        if in_str:
            if escape:
                escape = False
            elif c == "\\":
                escape = True
            elif c == '"':
                in_str = False
            i += 1
            continue
        if c == '"':
            in_str = True
            i += 1
            continue
        if c == "#":
            line_comment = True
            i += 1
            continue
        if c == "/" and n == "/":
            line_comment = True
            i += 2
            continue
        if c == "/" and n == "*":
            block_comment = True
            i += 2
            continue
        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                return text[open_pos + 1 : i], i + 1
        i += 1
    return text[open_pos + 1 :], len(text)


def _attrs(body: str) -> dict[str, str]:
    # Top-level-ish attributes with multiline expression support.
    out: dict[str, str] = {}
    lines = body.splitlines()
    index = 0
    while index < len(lines):
        stripped = lines[index].strip()
        if not stripped or stripped.startswith(("#", "//")):
            index += 1
            continue
        match = re.match(r"^([A-Za-z_][\w-]*)\s*=\s*(.+)$", stripped)
        if not match:
            index += 1
            continue
        key = match.group(1)
        parts = [match.group(2).strip()]
        depth = parts[0].count("{") + parts[0].count("[") + parts[0].count("(")
        depth -= parts[0].count("}") + parts[0].count("]") + parts[0].count(")")
        index += 1
        while depth > 0 and index < len(lines):
            part = lines[index].strip()
            parts.append(part)
            depth += part.count("{") + part.count("[") + part.count("(")
            depth -= part.count("}") + part.count("]") + part.count(")")
            index += 1
        out[key] = "\n".join(parts).strip()
    return out


def _clean_string(value: str | None) -> str | None:
    if not value:
        return None
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] == '"':
        return value[1:-1]
    return value


def _split_quoted_items(expr: str) -> list[str]:
    return [m.group(1) for m in re.finditer(r'"([^"\\]*(?:\\.[^"\\]*)*)"', expr)]


def _statement_blocks(body: str) -> list[str]:
    blocks: list[str] = []
    for match in re.finditer(r'(?m)^\s*statement\s*\{', body):
        block, _ = _balanced_block(body, match.end() - 1)
        blocks.append(block)
    return blocks


def _principal_blocks(body: str) -> list[str]:
    blocks: list[str] = []
    for match in re.finditer(r'(?m)^\s*principals\s*\{', body):
        block, _ = _balanced_block(body, match.end() - 1)
        blocks.append(block)
    return blocks


def _iam_statement_from_block(body: str) -> IamStatement:
    attrs = _attrs(body)
    principals: list[str] = []
    for principal_body in _principal_blocks(body):
        principal_attrs = _attrs(principal_body)
        principal_type = _clean_string(principal_attrs.get("type"))
        identifiers = _split_quoted_items(principal_attrs.get("identifiers", ""))
        if principal_type and identifiers:
            principals.extend([f"{principal_type}:{identifier}" for identifier in identifiers])
        else:
            principals.extend(identifiers)
    return IamStatement(
        sid=_clean_string(attrs.get("sid")),
        effect=_clean_string(attrs.get("effect")),
        actions=_split_quoted_items(attrs.get("actions", "")),
        not_actions=_split_quoted_items(attrs.get("not_actions", "")),
        resources=_split_quoted_items(attrs.get("resources", "")),
        not_resources=_split_quoted_items(attrs.get("not_resources", "")),
        principals=principals,
    )


def _jsonencode_object(expr: str) -> str | None:
    expr = expr.strip()
    if not expr.startswith("jsonencode("):
        return None
    start = expr.find("(")
    if start < 0:
        return None
    depth = 0
    in_str = False
    escape = False
    for index in range(start, len(expr)):
        char = expr[index]
        if in_str:
            if escape:
                escape = False
            elif char == "\\":
                escape = True
            elif char == '"':
                in_str = False
            continue
        if char == '"':
            in_str = True
            continue
        if char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
            if depth == 0:
                return expr[start + 1 : index].strip()
    return None


def _first_bracket_content(expr: str, open_char: str, close_char: str) -> str | None:
    start = expr.find(open_char)
    if start < 0:
        return None
    depth = 0
    in_str = False
    escape = False
    for index in range(start, len(expr)):
        char = expr[index]
        if in_str:
            if escape:
                escape = False
            elif char == "\\":
                escape = True
            elif char == '"':
                in_str = False
            continue
        if char == '"':
            in_str = True
            continue
        if char == open_char:
            depth += 1
        elif char == close_char:
            depth -= 1
            if depth == 0:
                return expr[start + 1 : index]
    return None


def _object_value(expr: str, key: str) -> str | None:
    match = re.search(rf'(?m)(?:^|[{{,\n])\s*{re.escape(key)}\s*=\s*', expr)
    if not match:
        return None
    index = match.end()
    depth_brace = 0
    depth_bracket = 0
    in_str = False
    escape = False
    value_start = index
    while index < len(expr):
        char = expr[index]
        if in_str:
            if escape:
                escape = False
            elif char == "\\":
                escape = True
            elif char == '"':
                in_str = False
            index += 1
            continue
        if char == '"':
            in_str = True
            index += 1
            continue
        if char == "{":
            depth_brace += 1
        elif char == "}":
            if depth_brace == 0 and depth_bracket == 0:
                break
            depth_brace = max(depth_brace - 1, 0)
        elif char == "[":
            depth_bracket += 1
        elif char == "]":
            depth_bracket = max(depth_bracket - 1, 0)
        elif char == "," and depth_brace == 0 and depth_bracket == 0:
            break
        elif char == "\n" and depth_brace == 0 and depth_bracket == 0:
            remainder = expr[index + 1 :]
            if re.match(r"^\s*[A-Za-z_][\w-]*\s*=", remainder):
                break
        index += 1
    return expr[value_start:index].strip()


def _object_list(expr: str, key: str) -> list[str]:
    value = _object_value(expr, key)
    if not value:
        return []
    if value.strip().startswith("["):
        return _split_quoted_items(_first_bracket_content(value, "[", "]") or "")
    single = _clean_string(value)
    return [single] if single else []


def _inline_statement_objects(expr: str) -> list[str]:
    statement_expr = _object_value(expr, "Statement")
    if not statement_expr:
        return []
    stripped = statement_expr.strip()
    if stripped.startswith("{"):
        body = _first_bracket_content(stripped, "{", "}")
        return [body] if body is not None else []
    if stripped.startswith("["):
        content = _first_bracket_content(stripped, "[", "]") or ""
        objects: list[str] = []
        index = 0
        while index < len(content):
            if content[index] == "{":
                body, next_index = _balanced_block(content, index)
                objects.append(body)
                index = next_index
            else:
                index += 1
        return objects
    return []


def _iam_statement_from_json_object(body: str) -> IamStatement:
    principals: list[str] = []
    principal_expr = _object_value(body, "Principal")
    if principal_expr:
        stripped = principal_expr.strip()
        if stripped.startswith("{"):
            principal_body = _first_bracket_content(stripped, "{", "}") or ""
            for principal_type in ["AWS", "Service", "Federated", "CanonicalUser"]:
                for identifier in _object_list(principal_body, principal_type):
                    principals.append(f"{principal_type}:{identifier}")
        else:
            principal = _clean_string(stripped)
            if principal:
                principals.append(principal)
    return IamStatement(
        sid=_clean_string(_object_value(body, "Sid")),
        effect=_clean_string(_object_value(body, "Effect")),
        actions=_object_list(body, "Action"),
        not_actions=_object_list(body, "NotAction"),
        resources=_object_list(body, "Resource"),
        not_resources=_object_list(body, "NotResource"),
        principals=principals,
    )


def _attachment_policy_targets(policy_expr: str) -> list[str]:
    return re.findall(r'(?:data\.)?aws_iam_policy(?:_document)?\.[A-Za-z_][\w-]*', policy_expr)


def _extract_iam_policy_facts(model: TerraformModel) -> None:
    facts: dict[str, IamPolicyFact] = {}
    attachment_refs: dict[str, list[str]] = {}
    for resource in model.resources:
        if resource.type == "aws_iam_policy_document":
            statements = [_iam_statement_from_block(block) for block in _statement_blocks(resource.body or "")]
            facts[resource.address] = IamPolicyFact(
                address=resource.address,
                source_kind="data" if resource.kind == "data" else "resource",
                name=resource.name,
                file=resource.file,
                statements=statements,
            )
        elif resource.type == "aws_iam_policy":
            policy_expr = resource.attributes.get("policy")
            statements: list[IamStatement] = []
            json_body = _jsonencode_object(policy_expr or "")
            if json_body:
                statements = [_iam_statement_from_json_object(body) for body in _inline_statement_objects(json_body)]
            facts[resource.address] = IamPolicyFact(
                address=resource.address,
                source_kind="resource",
                name=resource.name,
                file=resource.file,
                statements=statements,
                raw_policy=policy_expr,
            )
        elif resource.type in _ATTACHMENT_TARGETS:
            policy_arn = resource.attributes.get("policy_arn", "")
            target_kind = _ATTACHMENT_TARGETS[resource.type]
            target_value = _clean_string(resource.attributes.get(target_kind)) or resource.attributes.get(target_kind, "")
            label = f"{target_kind}:{target_value}" if target_value else target_kind
            for match in _attachment_policy_targets(policy_arn):
                attachment_refs.setdefault(match, []).append(label)

    for address, targets in attachment_refs.items():
        fact = facts.get(address)
        if fact:
            fact.attachments = sorted(set(targets))

    model.iam_policies = sorted(facts.values(), key=lambda item: item.address)


def parse_terraform(root: Path, source_root: Path | None = None) -> TerraformModel:
    root = root.resolve()
    source_root = (source_root or root).resolve()
    model = TerraformModel(root=source_root)
    for path in sorted(root.rglob("*.tf")):
        if any(p in {".terraform", ".git"} for p in path.parts) or not should_read(path, source_root):
            continue
        rel = path.relative_to(source_root).as_posix()
        model.source_files.append(rel)
        text = path.read_text(encoding="utf-8")
        for m in BLOCK_RE.finditer(text):
            kind, first, second = m.groups()
            body, _ = _balanced_block(text, m.end() - 1)
            attrs = _attrs(body)
            refs = set(REF_RE.findall(body))
            if kind in ("resource", "data"):
                model.resources.append(Resource(kind, first, second or "", rel, attrs, refs, body))
            elif kind == "module":
                model.modules.append(Module(first, _clean_string(attrs.get("source")), rel, attrs, refs))
            elif kind == "variable":
                default = attrs.get("default")
                model.variables.append(
                    Variable(
                        first,
                        attrs.get("type"),
                        _clean_string(attrs.get("description")),
                        default,
                        attrs.get("sensitive", "false").lower() == "true",
                        rel,
                    )
                )
            elif kind == "output":
                model.outputs.append(
                    Output(
                        first,
                        _clean_string(attrs.get("description")),
                        attrs.get("value"),
                        attrs.get("sensitive", "false").lower() == "true",
                        rel,
                    )
                )
            elif kind == "provider":
                if not any(p.name == first for p in model.providers):
                    model.providers.append(Provider(first))
    _merge_required_providers(model)
    _extract_iam_policy_facts(model)
    return model


def _merge_required_providers(model: TerraformModel) -> None:
    # Lightweight extraction from required_providers; enough for common Terraform syntax.
    for rel in model.source_files:
        text = (model.root / rel).read_text(encoding="utf-8")
        idx = text.find("required_providers")
        if idx < 0:
            continue
        brace = text.find("{", idx)
        if brace < 0:
            continue
        body, _ = _balanced_block(text, brace)
        for pm in re.finditer(r"(?ms)^\s*([A-Za-z_][\w-]*)\s*=\s*\{(.*?)^\s*\}", body):
            name, pbody = pm.group(1), pm.group(2)
            src = re.search(r'(?m)^\s*source\s*=\s*"([^"]+)"', pbody)
            ver = re.search(r'(?m)^\s*version\s*=\s*"([^"]+)"', pbody)
            existing = next((p for p in model.providers if p.name == name), None)
            if existing:
                existing.source = src.group(1) if src else existing.source
                existing.version = ver.group(1) if ver else existing.version
            else:
                model.providers.append(Provider(name, src.group(1) if src else None, ver.group(1) if ver else None))


def terraform_docs_json(root: Path) -> dict[str, Any] | None:
    exe = shutil.which("terraform-docs")
    if not exe:
        return None
    try:
        proc = subprocess.run([exe, "json", str(root)], capture_output=True, text=True, check=False, timeout=30)
    except (subprocess.TimeoutExpired, OSError):
        return None
    if proc.returncode != 0 or len(proc.stdout.encode("utf-8", errors="ignore")) > MAX_SUBPROCESS_OUTPUT:
        return None
    try:
        return json.loads(proc.stdout)
    except json.JSONDecodeError:
        return None


def terraform_docs_markdown(root: Path) -> str | None:
    exe = shutil.which("terraform-docs")
    if not exe:
        return None
    try:
        proc = subprocess.run(
            [exe, "markdown", "table", str(root)], capture_output=True, text=True, check=False, timeout=30
        )
    except (subprocess.TimeoutExpired, OSError):
        return None
    if proc.returncode != 0:
        return None
    text = proc.stdout.strip()
    if not text:
        return None
    if len(text.encode("utf-8", errors="ignore")) > MAX_SUBPROCESS_OUTPUT:
        return None
    return text


def enrich_from_terraform_docs(model: TerraformModel, doc: dict[str, Any] | None) -> TerraformModel:
    if not doc:
        return model
    inputs = doc.get("inputs") or []
    # terraform-docs JSON commonly emits lists of objects; support map form too.
    if isinstance(inputs, dict):
        inputs = [dict({"name": k}, **(v or {})) for k, v in inputs.items()]
    by_name = {v.name: v for v in model.variables}
    for item in inputs:
        if not isinstance(item, dict):
            continue
        v = by_name.get(item.get("name"))
        if v:
            v.description = item.get("description") or v.description
            if item.get("type") is not None:
                v.type = str(item.get("type"))
            if "default" in item:
                v.default = item["default"]
            v.sensitive = bool(item.get("sensitive", v.sensitive))
    outputs = doc.get("outputs") or []
    if isinstance(outputs, dict):
        outputs = [dict({"name": k}, **(v or {})) for k, v in outputs.items()]
    ob = {o.name: o for o in model.outputs}
    for item in outputs:
        if not isinstance(item, dict):
            continue
        o = ob.get(item.get("name"))
        if o:
            o.description = item.get("description") or o.description
            o.sensitive = bool(item.get("sensitive", o.sensitive))
    return model
