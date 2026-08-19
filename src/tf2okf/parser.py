from __future__ import annotations

import json
import re
import shutil
import subprocess
from pathlib import Path
from typing import Any

from .model import Module, Output, Provider, Resource, TerraformModel, Variable
from .security import MAX_SUBPROCESS_OUTPUT, should_read

BLOCK_RE = re.compile(r'(?m)^\s*(resource|data|module|variable|output|provider)\s+"([^"]+)"(?:\s+"([^"]+)")?\s*\{')
REF_RE = re.compile(
    r"\b(?:data\.)?[A-Za-z_][\w-]*\.[A-Za-z_][\w-]*(?:\.[A-Za-z_][\w-]*)?|\bmodule\.[A-Za-z_][\w-]*|\bvar\.[A-Za-z_][\w-]*|\blocal\.[A-Za-z_][\w-]*"
)
ATTR_RE = re.compile(r"(?m)^\s*([A-Za-z_][\w-]*)\s*=\s*(.+?)\s*$")


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
    # Top-level-ish line attributes. This intentionally preserves expressions as text.
    out = {}
    depth = 0
    for line in body.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith(("#", "//")):
            continue
        if depth == 0:
            m = re.match(r"^([A-Za-z_][\w-]*)\s*=\s*(.+)$", stripped)
            if m:
                out[m.group(1)] = m.group(2).strip()
        depth += line.count("{") + line.count("[") - line.count("}") - line.count("]")
        depth = max(depth, 0)
    return out


def _clean_string(value: str | None) -> str | None:
    if not value:
        return None
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] == '"':
        return value[1:-1]
    return value


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
                model.resources.append(Resource(kind, first, second or "", rel, attrs, refs))
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
