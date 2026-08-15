from pathlib import Path
from typer.testing import CliRunner
from tf2okf.cli import app
from tf2okf.config import load
from tf2okf.frameworks import detect, discover_terragrunt

runner=CliRunner()

def test_detect_plain_terraform(tmp_path: Path):
    (tmp_path/'main.tf').write_text('resource "null_resource" "x" {}')
    d=detect(tmp_path,load(tmp_path))
    assert d.framework=='plain-terraform'

def test_detect_terragrunt_and_generate(tmp_path: Path):
    (tmp_path/'root.hcl').write_text('locals { project = "demo" }')
    vpc=tmp_path/'live'/'dev'/'vpc'; appdir=tmp_path/'live'/'dev'/'app'
    vpc.mkdir(parents=True); appdir.mkdir(parents=True)
    (vpc/'terragrunt.hcl').write_text('''terraform {\n source = "git::https://example.com/modules.git//vpc?ref=v1"\n}\ninclude "root" { path = find_in_parent_folders("root.hcl") }\n''')
    (appdir/'terragrunt.hcl').write_text('''terraform {\n source = "git::https://example.com/modules.git//app?ref=v1"\n}\ndependency "vpc" {\n config_path = "../vpc"\n}\n''')
    cfg=load(tmp_path); d=detect(tmp_path,cfg)
    assert d.framework=='terragrunt'
    model=discover_terragrunt(tmp_path,cfg)
    assert len(model.units)==2
    assert any(u.dependencies==['../vpc'] for u in model.units)
    r=runner.invoke(app,['init',str(tmp_path)])
    assert r.exit_code==0, r.output
    assert (tmp_path/'.okf/generated/dependencies.md').exists()
    assert 'Terragrunt' in (tmp_path/'.okf/index.md').read_text()
    assert 'Terragrunt' in (tmp_path/'.github/copilot-instructions.md').read_text()

def test_explicit_framework_override(tmp_path: Path):
    (tmp_path/'components').mkdir(); (tmp_path/'bin').mkdir(); (tmp_path/'bin'/'terraform.sh').write_text('')
    (tmp_path/'main.tf').write_text('resource "null_resource" "x" {}')
    cfg=load(tmp_path); cfg['framework']['type']='plain-terraform'
    d=detect(tmp_path,cfg)
    assert d.framework=='plain-terraform' and d.confidence==100

def test_detect_tfscaffold_high_confidence(tmp_path: Path):
    (tmp_path/'bin').mkdir()
    (tmp_path/'bin'/'terraform.sh').write_text('#!/bin/bash\n')
    component = tmp_path/'components'/'app'
    component.mkdir(parents=True)
    (component/'main.tf').write_text('resource "null_resource" "x" {}')
    module = tmp_path/'modules'/'tags'
    module.mkdir(parents=True)
    (module/'main.tf').write_text('output "x" { value = "x" }')
    etc = tmp_path/'etc'
    etc.mkdir()
    (etc/'env_eu-west-1_dev.tfvars').write_text('environment = "dev"\n')
    (etc/'versions_eu-west-1_dev.tfvars').write_text('app_version = "1"\n')
    d=detect(tmp_path,load(tmp_path))
    assert d.framework=='tfscaffold'
    assert d.confidence >= 95
