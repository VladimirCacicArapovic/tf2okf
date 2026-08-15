from __future__ import annotations
from dataclasses import dataclass, field
from pathlib import Path
import re
from .model import TerraformModel
from .parser import parse_terraform, terraform_docs_json, terraform_docs_markdown, enrich_from_terraform_docs
from .scaffold import discover_tfscaffold

SUPPORTED = ('auto', 'plain-terraform', 'tfscaffold', 'terragrunt')

@dataclass
class Detection:
    framework: str
    confidence: int
    reasons: list[str] = field(default_factory=list)

@dataclass
class TerragruntUnit:
    name: str
    path: Path
    config_file: str
    terraform_source: str | None = None
    dependencies: list[str] = field(default_factory=list)
    includes: list[str] = field(default_factory=list)
    terraform: TerraformModel | None = None

@dataclass
class TerragruntModel:
    root: Path
    units: list[TerragruntUnit] = field(default_factory=list)
    stack_files: list[str] = field(default_factory=list)
    shared_hcl_files: list[str] = field(default_factory=list)


def _has_tf(repo: Path) -> bool:
    return any(p.is_file() for p in repo.rglob('*.tf') if '.terraform' not in p.parts and '.terragrunt-cache' not in p.parts)


def detect(repo: Path, cfg: dict | None = None) -> Detection:
    cfg = cfg or {}
    forced = cfg.get('framework', {}).get('type') or cfg.get('layout', {}).get('mode', 'auto')
    aliases = {'terraform': 'plain-terraform'}
    forced = aliases.get(forced, forced)
    if forced and forced != 'auto':
        if forced not in SUPPORTED:
            raise ValueError(f'Unsupported framework: {forced}. Supported: {", ".join(SUPPORTED)}')
        return Detection(forced, 100, [f'Explicitly selected in configuration: {forced}'])

    scores: dict[str, tuple[int, list[str]]] = {
        'tfscaffold': (0, []), 'terragrunt': (0, []), 'plain-terraform': (0, [])
    }
    def add(name: str, points: int, reason: str):
        score, reasons = scores[name]; scores[name] = (score + points, reasons + [reason])

    if (repo/'bin'/'terraform.sh').exists(): add('tfscaffold', 45, 'found bin/terraform.sh')
    if (repo/'components').is_dir(): add('tfscaffold', 25, 'found components/ directory')
    if (repo/'etc').is_dir() and any((repo/'etc').glob('*.tfvars*')): add('tfscaffold', 15, 'found tfvars under etc/')

    tg = [p for p in repo.rglob('terragrunt.hcl') if '.terragrunt-cache' not in p.parts and '.terragrunt-stack' not in p.parts]
    stacks = [p for p in repo.rglob('terragrunt.stack.hcl') if '.terragrunt-cache' not in p.parts and '.terragrunt-stack' not in p.parts]
    if tg: add('terragrunt', 70, f'found {len(tg)} terragrunt.hcl file(s)')
    if stacks: add('terragrunt', 15, f'found {len(stacks)} terragrunt.stack.hcl file(s)')
    if (repo/'root.hcl').exists(): add('terragrunt', 10, 'found root.hcl')

    if _has_tf(repo): add('plain-terraform', 30, 'found Terraform (*.tf) source')
    winner = max(scores.items(), key=lambda kv: kv[1][0])
    if winner[1][0] == 0:
        return Detection('plain-terraform', 10, ['no framework signature found; falling back to plain Terraform'])
    # Framework-specific signatures outrank plain Terraform if present.
    if scores['terragrunt'][0] >= 70: winner = ('terragrunt', scores['terragrunt'])
    elif scores['tfscaffold'][0] >= 45: winner = ('tfscaffold', scores['tfscaffold'])
    return Detection(winner[0], min(100, winner[1][0]), winner[1][1])


def _extract_block(text: str, keyword: str) -> list[str]:
    # Lightweight balanced-brace extraction; deterministic and dependency-free.
    starts = [m.start() for m in re.finditer(rf'(?m)^\s*{re.escape(keyword)}(?:\s+"[^"]+")?\s*\{{', text)]
    blocks=[]
    for start in starts:
        brace=text.find('{',start); depth=0
        for i in range(brace,len(text)):
            if text[i]=='{': depth += 1
            elif text[i]=='}':
                depth -= 1
                if depth==0:
                    blocks.append(text[start:i+1]); break
    return blocks


def discover_terragrunt(repo: Path, cfg: dict) -> TerragruntModel:
    tcfg = cfg.get('terragrunt', {})
    ignore = set(tcfg.get('ignore_dirs', ['.git','.terraform','.terragrunt-cache','.terragrunt-stack','.okf']))
    use_docs = cfg.get('sources', {}).get('terraform_docs', True)
    result = TerragruntModel(root=repo)
    configs=[]
    for p in repo.rglob('terragrunt.hcl'):
        if any(part in ignore for part in p.relative_to(repo).parts): continue
        configs.append(p)
    for p in sorted(configs):
        text=p.read_text(encoding='utf-8',errors='replace')
        rel=p.relative_to(repo).as_posix(); unit_rel=p.parent.relative_to(repo).as_posix()
        source=None
        for block in _extract_block(text,'terraform'):
            m=re.search(r'(?m)^\s*source\s*=\s*["\']([^"\']+)["\']',block)
            if m: source=m.group(1); break
        deps=[]
        for block in _extract_block(text,'dependency'):
            m=re.search(r'(?m)^\s*config_path\s*=\s*["\']([^"\']+)["\']',block)
            if m: deps.append(m.group(1))
        includes=[]
        for block in _extract_block(text,'include'):
            m=re.search(r'(?m)^\s*path\s*=\s*(.+)$',block)
            if m: includes.append(m.group(1).strip())
        tfmodel=None
        if any(p.parent.glob('*.tf')):
            tfmodel=parse_terraform(p.parent,source_root=repo)
            if use_docs:
                tfmodel=enrich_from_terraform_docs(tfmodel,terraform_docs_json(p.parent))
                tfmodel.terraform_docs_markdown = terraform_docs_markdown(p.parent)
        result.units.append(TerragruntUnit(name=unit_rel if unit_rel!='.' else p.parent.name or 'root',path=p.parent,config_file=rel,terraform_source=source,dependencies=deps,includes=includes,terraform=tfmodel))
    for p in sorted(repo.rglob('terragrunt.stack.hcl')):
        if not any(part in ignore for part in p.relative_to(repo).parts): result.stack_files.append(p.relative_to(repo).as_posix())
    unit_configs={u.config_file for u in result.units}
    for p in sorted(repo.rglob('*.hcl')):
        rel=p.relative_to(repo).as_posix()
        if rel in unit_configs or rel in result.stack_files or any(part in ignore for part in p.relative_to(repo).parts): continue
        result.shared_hcl_files.append(rel)
    return result


def discover(repo: Path, cfg: dict):
    d=detect(repo,cfg)
    if d.framework=='tfscaffold': return d, discover_tfscaffold(repo,cfg)
    if d.framework=='terragrunt': return d, discover_terragrunt(repo,cfg)
    root=(repo/cfg.get('terraform',{}).get('root','.')).resolve()
    model=parse_terraform(root,source_root=repo)
    if cfg.get('sources',{}).get('terraform_docs',True):
        model=enrich_from_terraform_docs(model,terraform_docs_json(root))
        model.terraform_docs_markdown = terraform_docs_markdown(root)
    return d, model
