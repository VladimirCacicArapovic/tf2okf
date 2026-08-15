from __future__ import annotations
from datetime import datetime, timezone
from pathlib import Path
import hashlib
import json
import re
import yaml
from .model import TerraformModel, Resource, Module
from . import __version__
from .security import redact_attribute

GENERATED_DIR = 'generated'

def _stamp() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00','Z')

def _fm(meta: dict) -> str:
    return '---\n' + yaml.safe_dump(meta, sort_keys=False, allow_unicode=True).strip() + '\n---\n\n'

def _source_entries(files: list[str], source_prefix: str) -> list[dict]:
    return [{'id': f'source-{i+1}', 'resource': f'{source_prefix}{f}', 'author': 'process:terraform'} for i,f in enumerate(sorted(set(files)))]

def _concept_meta(type_: str, title: str, description: str, files: list[str], tags: list[str], resource: str | None = None, source_prefix: str = '../../') -> dict:
    m = {'type': type_, 'title': title, 'description': description, 'tags': tags,
         'generated': {'by': f'tf2okf/{__version__}', 'at': _stamp()}}
    if resource: m['resource'] = resource
    if files: m['sources'] = _source_entries(files, source_prefix)
    return m

def _safe(name: str) -> str:
    return re.sub(r'[^a-z0-9._-]+','-',name.lower()).strip('-')

def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip()+'\n', encoding='utf-8')

def generate_bundle(model: TerraformModel, out: Path, config: dict, stable_timestamp: str | None = None) -> None:
    out.mkdir(parents=True, exist_ok=True)
    gen = out / GENERATED_DIR
    # tf2okf owns generated/ only.
    if gen.exists():
        for p in sorted(gen.rglob('*'), reverse=True):
            if p.is_file(): p.unlink()
            elif p.is_dir(): p.rmdir()
    gen.mkdir(parents=True, exist_ok=True)
    knowledge = out / 'knowledge'; knowledge.mkdir(exist_ok=True)
    arch = knowledge / 'architecture.md'
    if not arch.exists():
        _write(arch, _fm({'type':'Architecture Knowledge','title':'Architecture','description':'Human-curated architecture and design intent.','tags':['architecture','manual']}) + '# Architecture\n\nAdd the architectural **why**, constraints and decisions here. tf2okf will not overwrite this file.')
    sec = knowledge / 'security.md'
    if not sec.exists():
        _write(sec, _fm({'type':'Security Knowledge','title':'Security','description':'Human-curated security constraints and rationale.','tags':['security','manual']}) + '# Security\n\nAdd project-specific security requirements and rationale here. tf2okf will not overwrite this file.')

    if config['generation'].get('resources', True):
        for r in model.resources:
            _write_resource(gen / 'resources' / f'{_safe(r.address)}.md', r)
    if config['generation'].get('modules', True):
        for m in model.modules:
            _write_module(gen / 'modules' / f'{_safe(m.name)}.md', m)
    if config['generation'].get('inputs', True): _write_inputs(gen/'inputs.md', model)
    if config['generation'].get('outputs', True): _write_outputs(gen/'outputs.md', model)
    if config['generation'].get('providers', True): _write_providers(gen/'providers.md', model)
    if config['generation'].get('dependencies', True): _write_dependencies(gen/'dependencies.md', model)
    _write_generated_index(gen/'index.md', model)
    _write_root_index(out/'index.md', model)
    _write_manifest(out/'.tf2okf-manifest.json', model, out)

def _write_resource(path: Path, r: Resource) -> None:
    meta = _concept_meta('Terraform Data Source' if r.kind=='data' else 'Terraform Resource', r.address,
        f'{r.kind.title()} `{r.address}` defined in `{r.file}`.', [r.file], ['terraform', r.kind, r.type], f'terraform://{r.address}', source_prefix='../../../')
    lines = [
        _fm(meta),
        f'# {r.address}',
        '',
        f'This {r.kind} captures the declared configuration for `{r.address}` and the references it makes to other Terraform objects.',
        '',
        '## Source',
        '',
        f'- File: `{r.file}`',
        f'- Terraform address: `{r.address}`',
        f'- Kind: `{r.kind}`',
        f'- Type: `{r.type}`',
        '',
    ]
    if r.attributes:
        lines += ['## Configuration', '', '| Attribute | Expression |', '|---|---|']
        for k,v in sorted(r.attributes.items()):
            safe_v = redact_attribute(k, v)
            escaped_v = safe_v.replace('|', '\\|')
            lines.append(f'| `{k}` | `{escaped_v}` |')
        lines.append('')
    if r.references:
        lines += ['## References', ''] + [f'- `{x}`' for x in sorted(r.references)] + ['']
    _write(path, '\n'.join(lines))

def _write_module(path: Path, m: Module) -> None:
    meta = _concept_meta('Terraform Module', m.address, f'Module `{m.name}` sourced from `{m.source or "unknown"}`.', [m.file], ['terraform','module'], f'terraform://{m.address}', source_prefix='../../../')
    lines = [
        _fm(meta),
        f'# {m.address}',
        '',
        f'This module call records where `{m.address}` is declared, which module source it points at, and which Terraform objects it references.',
        '',
        f'- Source: `{m.source or "unknown"}`',
        f'- Defined in: `{m.file}`',
        '',
    ]
    if m.references: lines += ['## References','']+[f'- `{x}`' for x in sorted(m.references)]+['']
    _write(path,'\n'.join(lines))

def _write_inputs(path: Path, model: TerraformModel) -> None:
    meta = _concept_meta('Terraform Inputs','Terraform Inputs','Input variables exposed by this Terraform configuration.',[v.file for v in model.variables if v.file],['terraform','inputs'])
    lines=[
        _fm(meta),
        '# Terraform Inputs',
        '',
        'These inputs describe the values callers are expected to provide, along with defaults, sensitivity, and any captured descriptions.',
        '',
        '| Name | Type | Default | Sensitive | Description |',
        '|---|---|---|---|---|',
    ]
    for v in sorted(model.variables,key=lambda x:x.name):
        d = 'required' if v.default is None else str(v.default).replace('|', '\\|')
        description = (v.description or '').replace('|', '\\|')
        lines.append(f'| `{v.name}` | `{v.type or "any"}` | `{d}` | {str(v.sensitive).lower()} | {description} |')
    _write(path,'\n'.join(lines))

def _write_outputs(path: Path, model: TerraformModel) -> None:
    meta = _concept_meta('Terraform Outputs','Terraform Outputs','Outputs exposed by this Terraform configuration.',[o.file for o in model.outputs if o.file],['terraform','outputs'])
    lines=[
        _fm(meta),
        '# Terraform Outputs',
        '',
        'These outputs summarize the values this Terraform configuration exposes to callers or downstream stacks.',
        '',
        '| Name | Value | Sensitive | Description |',
        '|---|---|---|---|',
    ]
    for o in sorted(model.outputs,key=lambda x:x.name):
        value = (o.value or '').replace('|', '\\|')
        description = (o.description or '').replace('|', '\\|')
        lines.append(f'| `{o.name}` | `{value}` | {str(o.sensitive).lower()} | {description} |')
    _write(path,'\n'.join(lines))

def _write_providers(path: Path, model: TerraformModel) -> None:
    meta = _concept_meta('Terraform Providers','Terraform Providers','Providers used by this Terraform configuration.',model.source_files,['terraform','providers'])
    lines=[
        _fm(meta),
        '# Terraform Providers',
        '',
        'These providers were detected from the Terraform source and required provider declarations.',
        '',
        '| Name | Source | Version constraint |',
        '|---|---|---|',
    ]
    for p in sorted(model.providers,key=lambda x:x.name): lines.append(f'| `{p.name}` | `{p.source or ""}` | `{p.version or ""}` |')
    _write(path,'\n'.join(lines))

def _write_dependencies(path: Path, model: TerraformModel) -> None:
    meta = _concept_meta('Terraform Dependency Graph','Terraform Dependencies','Reference graph extracted from Terraform expressions.',model.source_files,['terraform','dependencies','graph'])
    nodes = {r.address for r in model.resources} | {m.address for m in model.modules}
    edges=[]
    for obj in [*model.resources,*model.modules]:
        for ref in obj.references:
            target = '.'.join(ref.split('.')[:3]) if ref.startswith('data.') else '.'.join(ref.split('.')[:2])
            if target in nodes and target != obj.address: edges.append((obj.address,target))
    lines=[
        _fm(meta),
        '# Terraform Dependencies',
        '',
        'This graph shows which resources or module calls refer to other Terraform objects in their expressions.',
        '',
        'Edges are `consumer → referenced dependency`.',
        '',
    ]
    if edges:
        lines += ['```mermaid','graph TD']
        ids={n:f'n{i}' for i,n in enumerate(sorted(nodes))}
        for n,i in ids.items(): lines.append(f'  {i}["{n}"]')
        for a,b in sorted(set(edges)): lines.append(f'  {ids[a]} --> {ids[b]}')
        lines += ['```','', '## Edges',''] + [f'- `{a}` → `{b}`' for a,b in sorted(set(edges))]
    else: lines.append('No inter-resource/module references were detected by the lightweight parser.')
    _write(path,'\n'.join(lines))

def _write_generated_index(path: Path, model: TerraformModel) -> None:
    lines=[
        '# Generated Terraform Knowledge',
        '',
        'This directory contains machine-generated summaries of Terraform structure, interfaces, providers, and dependency relationships.',
        '',
        '* [Inputs](inputs.md) - Terraform input variables.',
        '* [Outputs](outputs.md) - Terraform outputs.',
        '* [Providers](providers.md) - Terraform providers.',
        '* [Dependencies](dependencies.md) - Extracted reference graph.',
        '',
    ]
    if model.resources:
        lines += ['## Resources',''] + [f'* [{r.address}](resources/{_safe(r.address)}.md) - `{r.type}`.' for r in sorted(model.resources,key=lambda x:x.address)] + ['']
    if model.modules:
        lines += ['## Modules',''] + [f'* [{m.address}](modules/{_safe(m.name)}.md) - `{m.source or "unknown"}`.' for m in sorted(model.modules,key=lambda x:x.name)] + ['']
    if model.terraform_docs_markdown:
        lines += ['## terraform-docs', '', 'The section below is copied from `terraform-docs` when that tool is installed and returns content for this root.', '', model.terraform_docs_markdown, '']
    _write(path,'\n'.join(lines))

def _write_root_index(path: Path, model: TerraformModel) -> None:
    header='---\nokf_version: "0.2"\n---\n\n'
    body='''# Terraform Knowledge Bundle\n\nStart here. Machine-generated Terraform facts live under `generated/`; human-maintained context lives under `knowledge/`.\n\n## Generated knowledge\n\n* [Terraform knowledge](generated/) - Resources, modules, inputs, outputs, providers and dependencies.\n\n## Curated knowledge\n\n* [Architecture](knowledge/architecture.md) - Architectural intent and constraints.\n* [Security](knowledge/security.md) - Security requirements and rationale.\n\n## Source of truth\n\nTerraform source remains the implementation source of truth. If generated knowledge and Terraform differ, regenerate with `tf2okf generate`.\n'''
    _write(path,header+body)

def _write_manifest(path: Path, model: TerraformModel, out: Path) -> None:
    data={'tf2okf_version':__version__,'okf_version':'0.2','source_files':{},'generated_files':{}}
    for rel in model.source_files:
        p=model.root/rel; data['source_files'][rel]=hashlib.sha256(p.read_bytes()).hexdigest()
    for p in sorted((out/GENERATED_DIR).rglob('*.md')):
        data['generated_files'][p.relative_to(out).as_posix()]=_normalised_hash(p)
    path.write_text(json.dumps(data,indent=2,sort_keys=True)+'\n',encoding='utf-8')

def _normalised_hash(path: Path) -> str:
    text=path.read_text(encoding='utf-8')
    # generated.at is intentionally ignored for drift comparison.
    text=re.sub(r"(?m)^\s*at: ['\"]?[^\n'\"]+['\"]?\s*$",'  at: <timestamp>',text)
    return hashlib.sha256(text.encode()).hexdigest()
