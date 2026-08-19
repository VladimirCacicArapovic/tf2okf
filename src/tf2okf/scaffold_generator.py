from __future__ import annotations

import hashlib
import json
import os
import re
from pathlib import Path

from . import __version__
from .ai import generate_summary
from .generator import (
    _ai_enabled,
    _ai_output_path,
    _compact,
    _fm,
    _generation_enabled,
    _normalised_hash,
    _render_default,
    _render_output,
    _safe,
    _stamp,
    _write,
)
from .model import Module, Resource, TerraformModel
from .scaffold import TerraformUnit, TfScaffoldModel
from .security import redact_attribute

_LOGICAL_OUT: Path | None = None
_MANUAL_DESC_START = "<!-- tf2okf:manual-description-start -->"
_MANUAL_DESC_END = "<!-- tf2okf:manual-description-end -->"
_MANUAL_DESC_DEFAULT = (
    "Add a detailed description of what this component is for, how it is used, and any operational caveats. "
    "Anything between the marker comments is preserved by `tf2okf generate`."
)


def _relative_source(concept_path: Path, repo: Path, rel_file: str) -> str:
    target = (repo / rel_file).resolve()
    logical_path = concept_path.resolve()
    # check/diff render into a temporary directory; source links must still be
    # identical to links generated in the configured repository output path.
    if _LOGICAL_OUT is not None:
        try:
            logical_path.relative_to(_LOGICAL_OUT.resolve())
        except ValueError:
            parts = concept_path.parts
            if "generated" in parts:
                idx = len(parts) - 1 - list(reversed(parts)).index("generated")
                logical_path = _LOGICAL_OUT / Path(*parts[idx:])
    return Path(os.path.relpath(target, logical_path.parent.resolve())).as_posix()


def _preserved_manual_description(existing_text: str | None) -> str:
    if not existing_text:
        return _MANUAL_DESC_DEFAULT
    pattern = re.compile(
        re.escape(_MANUAL_DESC_START) + r"\n?(.*?)\n?" + re.escape(_MANUAL_DESC_END),
        re.S,
    )
    match = pattern.search(existing_text)
    if not match:
        return _MANUAL_DESC_DEFAULT
    content = match.group(1).strip("\n")
    return content or _MANUAL_DESC_DEFAULT


def _existing_component_descriptions(gen: Path) -> dict[str, str]:
    preserved: dict[str, str] = {}
    components = gen / "components"
    if not components.exists():
        return preserved
    for index in components.glob("*/index.md"):
        preserved[index.relative_to(gen).as_posix()] = _preserved_manual_description(index.read_text(encoding="utf-8"))
    return preserved


def _meta(
    type_: str,
    title: str,
    description: str,
    files: list[str],
    tags: list[str],
    concept_path: Path,
    repo: Path,
    resource: str | None = None,
) -> dict:
    meta = {
        "type": type_,
        "title": title,
        "description": description,
        "tags": tags,
        "generated": {"by": f"tf2okf/{__version__}", "at": _stamp()},
    }
    if resource:
        meta["resource"] = resource
    if files:
        meta["sources"] = [
            {
                "id": f"source-{i + 1}",
                "resource": _relative_source(concept_path, repo, f),
                "author": "process:terraform",
            }
            for i, f in enumerate(sorted(set(files)))
        ]
    return meta


def _write_resource(path: Path, r: Resource, repo: Path, unit: TerraformUnit) -> None:
    meta = _meta(
        "Terraform Data Source" if r.kind == "data" else "Terraform Resource",
        r.address,
        f"{r.kind.title()} `{r.address}` in tfscaffold {unit.kind} `{unit.name}`.",
        [r.file],
        ["terraform", "tfscaffold", unit.kind, unit.name, r.kind, r.type],
        path,
        repo,
        f"terraform://tfscaffold/{unit.kind}/{unit.name}/{r.address}",
    )
    lines = [
        _fm(meta),
        f"# {r.address}",
        "",
        f"- tfscaffold {unit.kind.title()}: `{unit.name}`",
        f"- File: `{r.file}`",
        f"- Terraform address: `{r.address}`",
        "",
    ]
    if r.attributes:
        lines += ["## Configuration", "", "| Attribute | Expression |", "|---|---|"]
        for k, v in sorted(r.attributes.items()):
            escaped_v = redact_attribute(k, v).replace("|", "\\|")
            lines.append(f"| `{k}` | `{escaped_v}` |")
        lines.append("")
    if r.references:
        lines += ["## References", ""] + [f"- `{x}`" for x in sorted(r.references)] + [""]
    _write(path, "\n".join(lines))


def _write_module_call(path: Path, m: Module, repo: Path, unit: TerraformUnit) -> None:
    meta = _meta(
        "Terraform Module Call",
        m.address,
        f"Module call `{m.name}` from tfscaffold {unit.kind} `{unit.name}`.",
        [m.file],
        ["terraform", "tfscaffold", unit.kind, unit.name, "module-call"],
        path,
        repo,
        f"terraform://tfscaffold/{unit.kind}/{unit.name}/{m.address}",
    )
    lines = [_fm(meta), f"# {m.address}", "", f"- Source: `{m.source or 'unknown'}`", f"- Defined in: `{m.file}`", ""]
    if m.references:
        lines += ["## References", ""] + [f"- `{x}`" for x in sorted(m.references)] + [""]
    _write(path, "\n".join(lines))


def _write_summary(
    path: Path, model: TerraformModel, repo: Path, unit: TerraformUnit, manual_description: str | None = None
) -> None:
    meta = _meta(
        "tfscaffold Terraform Unit",
        unit.name,
        f"Terraform {unit.kind} `{unit.name}` managed in a tfscaffold repository.",
        model.source_files,
        ["terraform", "tfscaffold", unit.kind, unit.name],
        path,
        repo,
    )
    description = manual_description or _MANUAL_DESC_DEFAULT
    lines = [
        _fm(meta),
        f"# {unit.name}",
        "",
        (
            f"This tfscaffold {unit.kind} summarizes the Terraform root under "
            f"`{unit.path.relative_to(repo).as_posix()}` and highlights its interface, "
            "dependencies, and generated references."
        ),
        "",
        f"Kind: **tfscaffold {unit.kind}**",
        "",
        f"Source directory: `{unit.path.relative_to(repo).as_posix()}`",
        "",
        f"- Resources/data sources: **{len(model.resources)}**",
        f"- Module calls: **{len(model.modules)}**",
        f"- Inputs: **{len(model.variables)}**",
        f"- Outputs: **{len(model.outputs)}**",
        "",
        "## Component description",
        "",
        _MANUAL_DESC_START,
        description,
        _MANUAL_DESC_END,
        "",
        "## Knowledge",
        "",
        "* [Inputs](inputs.md)",
        "* [Outputs](outputs.md)",
        "* [Providers](providers.md)",
        "* [Dependencies](dependencies.md)",
        "",
    ]
    if model.resources:
        lines += (
            ["## Resources and data sources", ""]
            + [
                f"* [{r.address}](resources/{_safe(r.address)}.md)"
                for r in sorted(model.resources, key=lambda x: x.address)
            ]
            + [""]
        )
    if model.modules:
        lines += (
            ["## Module calls", ""]
            + [f"* [{m.address}](module-calls/{_safe(m.name)}.md)" for m in sorted(model.modules, key=lambda x: x.name)]
            + [""]
        )
    if model.terraform_docs_markdown:
        lines += [
            "## terraform-docs",
            "",
            "The section below is copied from `terraform-docs` when that tool is available for this unit.",
            "",
            model.terraform_docs_markdown,
            "",
        ]
    _write(path, "\n".join(lines))


def _write_inputs(path: Path, model: TerraformModel, repo: Path, unit: TerraformUnit, compact: bool = False) -> None:
    meta = _meta(
        "Terraform Inputs",
        f"{unit.name} Inputs",
        f"Inputs for tfscaffold {unit.kind} `{unit.name}`.",
        [v.file for v in model.variables if v.file],
        ["terraform", "tfscaffold", unit.kind, "inputs"],
        path,
        repo,
    )
    lines = [_fm(meta), f"# {unit.name} Inputs", ""]
    if compact:
        lines += ["| Name | Type | Required | Default |", "|---|---|---|---|"]
    else:
        lines += [
            (
                "These inputs describe the values expected by this tfscaffold unit, "
                "including defaults and captured descriptions."
            ),
            "",
            "| Name | Type | Default | Sensitive | Description |",
            "|---|---|---|---|---|",
        ]
    for v in sorted(model.variables, key=lambda x: x.name):
        d = _render_default(v.default, v.sensitive, v.name)
        if compact:
            required = "yes" if v.default is None else "no"
            lines.append(f"| `{v.name}` | `{v.type or 'any'}` | {required} | `{d}` |")
        else:
            description = (v.description or "").replace("|", "\\|")
            lines.append(f"| `{v.name}` | `{v.type or 'any'}` | `{d}` | {str(v.sensitive).lower()} | {description} |")
    _write(path, "\n".join(lines))


def _write_outputs(path: Path, model: TerraformModel, repo: Path, unit: TerraformUnit, compact: bool = False) -> None:
    meta = _meta(
        "Terraform Outputs",
        f"{unit.name} Outputs",
        f"Outputs for tfscaffold {unit.kind} `{unit.name}`.",
        [o.file for o in model.outputs if o.file],
        ["terraform", "tfscaffold", unit.kind, "outputs"],
        path,
        repo,
    )
    lines = [_fm(meta), f"# {unit.name} Outputs", ""]
    if compact:
        lines += ["| Name | Sensitive |", "|---|---|"]
    else:
        lines += [
            "These outputs summarize what this tfscaffold unit exposes to other components or operators.",
            "",
            "| Name | Value | Sensitive | Description |",
            "|---|---|---|---|",
        ]
    for o in sorted(model.outputs, key=lambda x: x.name):
        if compact:
            lines.append(f"| `{o.name}` | {str(o.sensitive).lower()} |")
        else:
            value = _render_output(o.value, o.sensitive, o.name)
            description = (o.description or "").replace("|", "\\|")
            lines.append(f"| `{o.name}` | `{value}` | {str(o.sensitive).lower()} | {description} |")
    _write(path, "\n".join(lines))


def _write_providers(path: Path, model: TerraformModel, repo: Path, unit: TerraformUnit) -> None:
    meta = _meta(
        "Terraform Providers",
        f"{unit.name} Providers",
        f"Providers for tfscaffold {unit.kind} `{unit.name}`.",
        model.source_files,
        ["terraform", "tfscaffold", unit.kind, "providers"],
        path,
        repo,
    )
    lines = [
        _fm(meta),
        f"# {unit.name} Providers",
        "",
        "These providers were detected from the unit source and required provider declarations.",
        "",
        "| Name | Source | Version constraint |",
        "|---|---|---|",
    ]
    for p in sorted(model.providers, key=lambda x: x.name):
        lines.append(f"| `{p.name}` | `{p.source or ''}` | `{p.version or ''}` |")
    _write(path, "\n".join(lines))


def _write_dependencies(path: Path, model: TerraformModel, repo: Path, unit: TerraformUnit) -> None:
    meta = _meta(
        "Terraform Dependency Graph",
        f"{unit.name} Dependencies",
        f"Reference graph for tfscaffold {unit.kind} `{unit.name}`.",
        model.source_files,
        ["terraform", "tfscaffold", unit.kind, "dependencies"],
        path,
        repo,
    )
    nodes = {r.address for r in model.resources} | {m.address for m in model.modules}
    edges = []
    for obj in [*model.resources, *model.modules]:
        for ref in obj.references:
            target = ".".join(ref.split(".")[:3]) if ref.startswith("data.") else ".".join(ref.split(".")[:2])
            if target in nodes and target != obj.address:
                edges.append((obj.address, target))
    lines = [
        _fm(meta),
        f"# {unit.name} Dependencies",
        "",
        "This graph shows which resources or module calls in the unit refer to other Terraform objects.",
        "",
        "Edges are `consumer → referenced dependency`.",
        "",
    ]
    if edges:
        lines += ["```mermaid", "graph TD"]
        ids = {n: f"n{i}" for i, n in enumerate(sorted(nodes))}
        for n, i in ids.items():
            lines.append(f'  {i}["{n}"]')
        for a, b in sorted(set(edges)):
            lines.append(f"  {ids[a]} --> {ids[b]}")
        lines += ["```", ""]
    else:
        lines.append("No inter-resource/module references were detected.")
    _write(path, "\n".join(lines))


def _write_unit(base: Path, unit: TerraformUnit, repo: Path, cfg: dict, manual_description: str | None = None) -> None:
    model = unit.model
    compact = _compact(cfg)
    _write_summary(base / "index.md", model, repo, unit, manual_description)
    if _generation_enabled(cfg, "resources", True):
        for r in model.resources:
            _write_resource(base / "resources" / f"{_safe(r.address)}.md", r, repo, unit)
    if _generation_enabled(cfg, "modules", True):
        for m in model.modules:
            _write_module_call(base / "module-calls" / f"{_safe(m.name)}.md", m, repo, unit)
    if _generation_enabled(cfg, "inputs", True):
        _write_inputs(base / "inputs.md", model, repo, unit, compact=compact)
    if _generation_enabled(cfg, "outputs", True):
        _write_outputs(base / "outputs.md", model, repo, unit, compact=compact)
    if _generation_enabled(cfg, "providers", True):
        _write_providers(base / "providers.md", model, repo, unit)
    if _generation_enabled(cfg, "dependencies", True):
        _write_dependencies(base / "dependencies.md", model, repo, unit)


def _write_envs(path: Path, model: TfScaffoldModel) -> None:
    meta = {
        "type": "tfscaffold Environment Index",
        "title": "tfscaffold Environments",
        "description": "Environment/version variable files discovered from tfscaffold etc/.",
        "tags": ["terraform", "tfscaffold", "environments"],
        "generated": {"by": f"tf2okf/{__version__}", "at": _stamp()},
    }
    if model.tfvars_files:
        meta["sources"] = [
            {"id": f"source-{i + 1}", "resource": _relative_source(path, model.root, f), "author": "process:terraform"}
            for i, f in enumerate(model.tfvars_files)
        ]
    lines = [
        _fm(meta),
        "# tfscaffold Environments",
        "",
        f"- Environments discovered: **{len(model.environments)}**",
        f"- Regions discovered: **{len(model.regions)}**",
        "",
    ]
    if model.environments:
        lines += ["## Environments", ""] + [f"- `{x}`" for x in sorted(model.environments)] + [""]
    if model.regions:
        lines += ["## Regions", ""] + [f"- `{x}`" for x in sorted(model.regions)] + [""]
    if model.tfvars_files:
        lines += ["## Variable files", ""] + [f"- `{x}`" for x in model.tfvars_files] + [""]
    _write(path, "\n".join(lines))


def _module_target(source: str | None) -> str | None:
    if not source:
        return None
    match = re.match(r"^\.\./\.\./modules/([^/]+)$", source)
    if match:
        return match.group(1)
    return None


def _write_topology(path: Path, model: TfScaffoldModel) -> None:
    files = [u.path.relative_to(model.root).as_posix() + "/main.tf" for u in [*model.components, *model.modules]]
    meta = {
        "type": "tfscaffold Topology",
        "title": "tfscaffold Topology",
        "description": "Cross-component and shared-module composition map.",
        "tags": ["terraform", "tfscaffold", "topology"],
        "generated": {"by": f"tf2okf/{__version__}", "at": _stamp()},
    }
    if files:
        meta["sources"] = [
            {"id": f"source-{i + 1}", "resource": _relative_source(path, model.root, f), "author": "process:terraform"}
            for i, f in enumerate(sorted(files))
        ]
    lines = [_fm(meta), "# tfscaffold Topology", "", "```mermaid", "graph LR"]
    node_ids: dict[str, str] = {}

    def node_id(kind: str, name: str) -> str:
        key = f"{kind}:{name}"
        if key not in node_ids:
            node_ids[key] = f"n{len(node_ids)}"
        return node_ids[key]

    edges: set[tuple[str, str]] = set()
    for component in model.components:
        src_id = node_id("component", component.name)
        lines.append(f'  {src_id}["component/{component.name}"]')
    for shared in model.modules:
        dst_id = node_id("module", shared.name)
        lines.append(f'  {dst_id}["shared-module/{shared.name}"]')
    for component in model.components:
        src = node_id("component", component.name)
        for call in component.model.modules:
            target = _module_target(call.source)
            if target:
                dst = node_id("module", target)
                edges.add((src, dst))
    for src, dst in sorted(edges):
        lines.append(f"  {src} --> {dst}")
    lines += ["```", ""]
    if edges:
        lines += ["## Edges", ""] + [f"- `{src}` -> `{dst}`" for src, dst in sorted(edges)]
    else:
        lines += ["No component-to-shared-module edges detected."]
    _write(path, "\n".join(lines))


def _write_ai_overview(path: Path, model: TfScaffoldModel, cfg: dict) -> None:
    component_names = ", ".join(u.name for u in model.components[:20]) or "none"
    module_names = ", ".join(u.name for u in model.modules[:20]) or "none"
    prompt = (
        "Summarize tfscaffold infrastructure facts for engineers. "
        "Return markdown only with headings: '## Overview', '## Core Flows', '## Key Interfaces', '## Risks'. "
        "Keep under 190 words.\n\n"
        f"Components: {len(model.components)} ({component_names})\n"
        f"Shared modules: {len(model.modules)} ({module_names})\n"
        f"Environments: {', '.join(sorted(model.environments)) or 'none'}\n"
        f"Regions: {', '.join(sorted(model.regions)) or 'none'}\n"
    )
    provider, model_name, summary = generate_summary(prompt, cfg)
    meta = {
        "type": "AI Infrastructure Summary",
        "title": "AI Overview",
        "description": "Concise AI-generated tfscaffold summary for quick retrieval.",
        "tags": ["ai", "summary", "compact", "tfscaffold"],
        "generated": {"by": f"tf2okf/{__version__}", "at": _stamp()},
        "ai": {"provider": provider, "model": model_name},
    }
    _write(path, _fm(meta) + "# AI Overview\n\n" + summary + "\n")


def generate_tfscaffold_bundle(model: TfScaffoldModel, out: Path, cfg: dict) -> None:
    global _LOGICAL_OUT
    _LOGICAL_OUT = (model.root / cfg.get("output", {}).get("directory", ".okf")).resolve()
    out.mkdir(parents=True, exist_ok=True)
    gen = out / "generated"
    preserved_manual = _existing_component_descriptions(gen)
    if gen.exists():
        for p in sorted(gen.rglob("*"), reverse=True):
            if p.is_file():
                p.unlink()
            elif p.is_dir():
                p.rmdir()
    gen.mkdir(parents=True, exist_ok=True)
    knowledge = out / "knowledge"
    knowledge.mkdir(exist_ok=True)
    for name, title, tags, body in [
        (
            "architecture.md",
            "Architecture",
            ["architecture", "manual"],
            "Add tfscaffold architecture, component boundaries and design intent here.",
        ),
        (
            "security.md",
            "Security",
            ["security", "manual"],
            "Add project-specific security constraints and rationale here.",
        ),
    ]:
        p = knowledge / name
        if not p.exists():
            _write(
                p,
                _fm(
                    {
                        "type": f"{title} Knowledge",
                        "title": title,
                        "description": f"Human-curated {title.lower()} knowledge.",
                        "tags": tags,
                    }
                )
                + f"# {title}\n\n{body}\n\ntf2okf will not overwrite this file.",
            )

    for unit in model.components:
        key = Path("components") / unit.name / "index.md"
        _write_unit(gen / "components" / unit.name, unit, model.root, cfg, preserved_manual.get(key.as_posix()))
    for unit in model.modules:
        _write_unit(gen / "shared-modules" / unit.name, unit, model.root, cfg)
    _write_envs(gen / "environments.md", model)
    _write_topology(gen / "topology.md", model)

    gi = [
        "# Generated tfscaffold Knowledge",
        "",
        f"Components: **{len(model.components)}**  ",
        f"Shared modules: **{len(model.modules)}**",
        "",
        "* [Environments](environments.md) - Environment/version tfvars discovered under `etc/`.",
        "* [Topology](topology.md) - Component to shared-module composition graph.",
        "",
    ]
    if model.components:
        gi += (
            ["## Components", ""]
            + [f"* [{u.name}](components/{u.name}/) - independent Terraform root module." for u in model.components]
            + [""]
        )
    if model.modules:
        gi += (
            ["## Shared modules", ""]
            + [f"* [{u.name}](shared-modules/{u.name}/) - reusable Terraform module." for u in model.modules]
            + [""]
        )
    _write(gen / "index.md", "\n".join(gi))

    header = '---\nokf_version: "0.2"\n---\n\n'
    body = (
        "# tfscaffold Knowledge Bundle\n\n"
        "This repository uses tfscaffold. Start with the generated component index, then read only the "
        "component or shared module relevant to the task.\n\n"
        "## Generated knowledge\n\n"
        "* [tfscaffold generated knowledge](generated/) - Components, shared modules, environment metadata and "
        "Terraform facts.\n\n"
        "## Curated knowledge\n\n"
        "* [Architecture](knowledge/architecture.md)\n"
        "* [Security](knowledge/security.md)\n\n"
        "## Source of truth\n\n"
        "Terraform under `components/` and `modules/` remains the implementation source of truth. "
        "Environment/version values under `etc/` are indexed as configuration inputs.\n"
    )
    _write(out / "index.md", header + body)
    if _ai_enabled(cfg):
        _write_ai_overview(_ai_output_path(out, cfg) / "overview.md", model, cfg)

    manifest = {
        "tf2okf_version": __version__,
        "okf_version": "0.2",
        "layout": "tfscaffold",
        "source_files": {},
        "generated_files": {},
    }
    files = set(model.tfvars_files)
    for unit in [*model.components, *model.modules]:
        files.update(unit.model.source_files)
    for rel in sorted(files):
        p = model.root / rel
        if p.exists():
            manifest["source_files"][rel] = hashlib.sha256(p.read_bytes()).hexdigest()
    for p in sorted(gen.rglob("*.md")):
        manifest["generated_files"][p.relative_to(out).as_posix()] = _normalised_hash(p)
    (out / ".tf2okf-manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
