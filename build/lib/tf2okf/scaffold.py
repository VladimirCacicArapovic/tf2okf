from __future__ import annotations
from dataclasses import dataclass, field
from fnmatch import fnmatch
from pathlib import Path
import re
from .model import TerraformModel
from .parser import parse_terraform, terraform_docs_json, terraform_docs_markdown, enrich_from_terraform_docs

@dataclass
class TerraformUnit:
    name: str
    kind: str  # component | module
    path: Path
    model: TerraformModel

@dataclass
class TfScaffoldModel:
    root: Path
    components: list[TerraformUnit] = field(default_factory=list)
    modules: list[TerraformUnit] = field(default_factory=list)
    tfvars_files: list[str] = field(default_factory=list)
    environments: set[str] = field(default_factory=set)
    regions: set[str] = field(default_factory=set)


def is_tfscaffold(repo: Path, cfg: dict) -> bool:
    mode = cfg.get('layout', {}).get('mode', 'auto')
    if mode == 'tfscaffold':
        return True
    if mode == 'terraform':
        return False
    tcfg = cfg.get('tfscaffold', {})
    components = repo / tcfg.get('components_dir', 'components')
    wrapper = repo / 'bin' / 'terraform.sh'
    return components.is_dir() and wrapper.exists()


def _include(name: str, patterns: list[str]) -> bool:
    return any(fnmatch(name, p) for p in (patterns or ['*']))


def _parse_unit(repo: Path, path: Path, name: str, kind: str, use_docs: bool) -> TerraformUnit:
    model = parse_terraform(path, source_root=repo)
    if use_docs:
        model = enrich_from_terraform_docs(model, terraform_docs_json(path))
        model.terraform_docs_markdown = terraform_docs_markdown(path)
    return TerraformUnit(name=name, kind=kind, path=path, model=model)


def discover_tfscaffold(repo: Path, cfg: dict) -> TfScaffoldModel:
    tcfg = cfg.get('tfscaffold', {})
    use_docs = cfg.get('sources', {}).get('terraform_docs', True)
    result = TfScaffoldModel(root=repo)

    components_dir = repo / tcfg.get('components_dir', 'components')
    patterns = tcfg.get('include_components', ['*'])
    if components_dir.is_dir():
        for child in sorted(components_dir.iterdir()):
            if not child.is_dir() or not _include(child.name, patterns):
                continue
            if any(child.glob('*.tf')):
                result.components.append(_parse_unit(repo, child, child.name, 'component', use_docs))

    if tcfg.get('include_modules', True):
        modules_dir = repo / tcfg.get('modules_dir', 'modules')
        if modules_dir.is_dir():
            for child in sorted(modules_dir.iterdir()):
                if child.is_dir() and any(child.glob('*.tf')):
                    result.modules.append(_parse_unit(repo, child, child.name, 'module', use_docs))

    variables_dir = repo / tcfg.get('variables_dir', 'etc')
    if variables_dir.is_dir():
        for p in sorted(list(variables_dir.glob('*.tfvars')) + list(variables_dir.glob('*.tfvars.json'))):
            rel = p.relative_to(repo).as_posix()
            result.tfvars_files.append(rel)
            # tfscaffold's common convention: env_<region>_<environment>.tfvars / versions_<region>_<environment>.tfvars
            m = re.match(r'^(?:env|versions)_([^_]+)_(.+?)\.tfvars(?:\.json)?$', p.name)
            if m:
                result.regions.add(m.group(1))
                result.environments.add(m.group(2))
    return result
