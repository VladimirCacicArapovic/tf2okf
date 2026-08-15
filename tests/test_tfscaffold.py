from pathlib import Path
from typer.testing import CliRunner
from tf2okf.cli import app
from tf2okf.config import load
from tf2okf.scaffold import is_tfscaffold, discover_tfscaffold

runner=CliRunner()

def make_repo(root: Path):
    (root/'bin').mkdir(); (root/'bin'/'terraform.sh').write_text('#!/bin/bash\n')
    for name,bucket in [('network','net'),('data','data')]:
        p=root/'components'/name; p.mkdir(parents=True)
        (p/'main.tf').write_text(f'''variable "environment" {{ type = string }}\nresource "aws_s3_bucket" "main" {{ bucket = "${{var.environment}}-{bucket}" }}\n''')
    m=root/'modules'/'tags'; m.mkdir(parents=True)
    (m/'main.tf').write_text('variable "environment" { type = string }\noutput "env" { value = var.environment }\n')
    e=root/'etc'; e.mkdir()
    (e/'env_eu-west-2_dev.tfvars').write_text('environment = "dev"\n')
    (e/'versions_eu-west-2_dev.tfvars').write_text('app_version = "1"\n')

def test_tfscaffold_discovery_and_namespacing(tmp_path: Path):
    make_repo(tmp_path)
    cfg=load(tmp_path)
    assert is_tfscaffold(tmp_path,cfg)
    sm=discover_tfscaffold(tmp_path,cfg)
    assert {u.name for u in sm.components} == {'network','data'}
    assert {u.name for u in sm.modules} == {'tags'}
    assert sm.environments == {'dev'}
    assert sm.regions == {'eu-west-2'}

    r=runner.invoke(app,['init',str(tmp_path)])
    assert r.exit_code == 0, r.output
    assert (tmp_path/'.okf/generated/components/network/resources/aws_s3_bucket.main.md').exists()
    assert (tmp_path/'.okf/generated/components/data/resources/aws_s3_bucket.main.md').exists()
    assert (tmp_path/'.okf/generated/shared-modules/tags/index.md').exists()
    assert 'dev' in (tmp_path/'.okf/generated/environments.md').read_text()
    copilot=(tmp_path/'.github/copilot-instructions.md').read_text()
    assert 'tfscaffold' in copilot
    assert 'independent root module/state boundary' in copilot

    r=runner.invoke(app,['check',str(tmp_path)])
    assert r.exit_code == 0, r.output
    (tmp_path/'components/network/main.tf').write_text('resource "aws_s3_bucket" "main" { bucket = "changed" }\n')
    r=runner.invoke(app,['check',str(tmp_path)])
    assert r.exit_code == 1
    assert 'components/network' in r.output
