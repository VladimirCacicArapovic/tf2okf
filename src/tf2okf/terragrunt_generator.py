from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path

from . import __version__
from .ai import generate_summary
from .frameworks import TerragruntModel
from .generator import _ai_enabled, _ai_output_path, _compact, _fm, _normalised_hash, _stamp, _write

_LOGICAL_OUT: Path | None = None


def _rel_source(concept: Path, repo: Path, rel: str) -> str:
    target = (repo / rel).resolve()
    logical = concept.resolve()
    if _LOGICAL_OUT is not None:
        try:
            logical.relative_to(_LOGICAL_OUT.resolve())
        except ValueError:
            parts = concept.parts
            if "generated" in parts:
                idx = len(parts) - 1 - list(reversed(parts)).index("generated")
                logical = _LOGICAL_OUT / Path(*parts[idx:])
    return Path(os.path.relpath(target, logical.parent.resolve())).as_posix()


def generate_terragrunt_bundle(model: TerragruntModel, out: Path, cfg: dict) -> None:
    global _LOGICAL_OUT
    _LOGICAL_OUT = (model.root / cfg.get("output", {}).get("directory", ".okf")).resolve()
    out.mkdir(parents=True, exist_ok=True)
    gen = out / "generated"
    if gen.exists():
        for p in sorted(gen.rglob("*"), reverse=True):
            if p.is_file():
                p.unlink()
            elif p.is_dir():
                p.rmdir()
    gen.mkdir(parents=True, exist_ok=True)
    (out / "knowledge").mkdir(exist_ok=True)
    for name, title, body in [
        ("architecture.md", "Architecture", "Add Terragrunt stack/unit architecture and design intent here."),
        ("security.md", "Security", "Add project-specific security constraints and rationale here."),
    ]:
        p = out / "knowledge" / name
        if not p.exists():
            _write(
                p,
                _fm({"type": f"{title} Knowledge", "title": title, "tags": ["manual", title.lower()]})
                + f"# {title}\n\n{body}\n\ntf2okf will not overwrite this file.\n",
            )
    compact = _compact(cfg)
    links = []
    for i, u in enumerate(model.units, 1):
        slug = f"unit-{i:03d}"
        path = gen / "units" / slug / "index.md"
        files = [u.config_file] + (u.terraform.source_files if u.terraform else [])
        meta = {
            "type": "Terragrunt Unit",
            "title": u.name,
            "description": f"Terragrunt unit at `{u.name}`.",
            "tags": ["terragrunt", "unit"],
            "generated": {"by": f"tf2okf/{__version__}", "at": _stamp()},
            "sources": [
                {"id": f"source-{n + 1}", "resource": _rel_source(path, model.root, f), "author": "process:terraform"}
                for n, f in enumerate(files)
            ],
        }
        lines = [
            _fm(meta),
            f"# {u.name}",
            "",
            f"- Config: `{u.config_file}`",
            f"- Terraform source: `{u.terraform_source or 'not statically detected'}`",
            "",
        ]
        if u.dependencies:
            lines += ["## Terragrunt dependencies", ""] + [f"- `{d}`" for d in u.dependencies] + [""]
        if u.includes and not compact:
            lines += ["## Includes", ""] + [f"- `{x}`" for x in u.includes] + [""]
        if u.terraform:
            lines += [
                "## Local Terraform facts",
                "",
                f"- Resources/data sources: **{len(u.terraform.resources)}**",
                f"- Module calls: **{len(u.terraform.modules)}**",
                f"- Inputs: **{len(u.terraform.variables)}**",
                f"- Outputs: **{len(u.terraform.outputs)}**",
                "",
            ]
        _write(path, "\n".join(lines))
        links.append(f"* [{u.name}](units/{slug}/)")
    # Cross-unit graph from static config_path values.
    gp = gen / "dependencies.md"
    meta = {
        "type": "Terragrunt Dependency Graph",
        "title": "Terragrunt Dependencies",
        "tags": ["terragrunt", "dependencies"],
        "generated": {"by": f"tf2okf/{__version__}", "at": _stamp()},
    }
    lines = [
        _fm(meta),
        "# Terragrunt Dependencies",
        "",
        "Static `dependency.config_path` relationships detected from unit configs.",
        "",
        "```mermaid",
        "graph TD",
    ]
    ids = {u.name: f"u{i}" for i, u in enumerate(model.units)}
    for name, id_ in ids.items():
        lines.append(f'  {id_}["{name}"]')
    for u in model.units:
        for dep in u.dependencies:
            try:
                target = (u.path / dep).resolve().relative_to(model.root.resolve()).as_posix()
            except Exception:
                continue
            if target in ids:
                lines.append(f"  {ids[u.name]} --> {ids[target]}")
    lines += ["```", ""]
    _write(gp, "\n".join(lines))
    idx = (
        [
            "# Generated Terragrunt Knowledge",
            "",
            f"Units: **{len(model.units)}**  ",
            f"Stack definitions: **{len(model.stack_files)}**",
            "",
            "* [Dependency graph](dependencies.md)",
            "",
            "## Units",
            "",
        ]
        + links
        + [""]
    )
    if model.stack_files:
        idx += ["## Stack definitions", ""] + [f"* `{p}`" for p in model.stack_files] + [""]
    if model.shared_hcl_files:
        idx += ["## Shared HCL", ""] + [f"* `{p}`" for p in model.shared_hcl_files] + [""]
    _write(gen / "index.md", "\n".join(idx))
    _write(
        out / "index.md",
        '---\nokf_version: "0.2"\n---\n\n# Terragrunt Knowledge Bundle\n\nStart with [generated knowledge](generated/) and read only the relevant unit.\n\n## Curated knowledge\n\n* [Architecture](knowledge/architecture.md)\n* [Security](knowledge/security.md)\n\nTerragrunt configuration and referenced Terraform/OpenTofu modules remain the implementation source of truth.\n',
    )
    if _ai_enabled(cfg):
        _write_terragrunt_ai_overview(_ai_output_path(out, cfg) / "overview.md", model, cfg)
    manifest = {
        "tf2okf_version": __version__,
        "okf_version": "0.2",
        "framework": "terragrunt",
        "source_files": {},
        "generated_files": {},
    }
    files = set(model.stack_files + model.shared_hcl_files + [u.config_file for u in model.units])
    for u in model.units:
        if u.terraform:
            files.update(u.terraform.source_files)
    for rel in sorted(files):
        p = model.root / rel
        if p.exists():
            manifest["source_files"][rel] = hashlib.sha256(p.read_bytes()).hexdigest()
    for p in sorted(gen.rglob("*.md")):
        manifest["generated_files"][p.relative_to(out).as_posix()] = _normalised_hash(p)
    (out / ".tf2okf-manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _write_terragrunt_ai_overview(path: Path, model: TerragruntModel, cfg: dict) -> None:
    names = ", ".join(u.name for u in model.units[:20]) or "none"
    prompt = (
        "Summarize Terragrunt structure for engineering handoff. "
        "Return markdown only with headings: '## Overview', '## Unit Relationships', '## Operational Notes', '## Risks'. "
        "Keep under 180 words.\n\n"
        f"Unit count: {len(model.units)}\n"
        f"Units: {names}\n"
        f"Stack files: {len(model.stack_files)}\n"
        f"Shared HCL files: {len(model.shared_hcl_files)}\n"
    )
    provider, model_name, summary = generate_summary(prompt, cfg)
    meta = {
        "type": "AI Infrastructure Summary",
        "title": "AI Overview",
        "description": "Concise AI-generated Terragrunt summary for quick retrieval.",
        "tags": ["ai", "summary", "compact", "terragrunt"],
        "generated": {"by": f"tf2okf/{__version__}", "at": _stamp()},
        "ai": {"provider": provider, "model": model_name},
    }
    _write(path, _fm(meta) + "# AI Overview\n\n" + summary + "\n")
