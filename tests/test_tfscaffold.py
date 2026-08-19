import re
from pathlib import Path

from typer.testing import CliRunner

from tf2okf.cli import app
from tf2okf.config import load
from tf2okf.scaffold import discover_tfscaffold, is_tfscaffold
from tf2okf.scaffold_generator import generate_tfscaffold_bundle

runner = CliRunner()


def make_repo(root: Path):
    (root / "bin").mkdir()
    (root / "bin" / "terraform.sh").write_text("#!/bin/bash\n")
    for name, bucket in [("network", "net"), ("data", "data")]:
        p = root / "components" / name
        p.mkdir(parents=True)
        content = (
            'variable "environment" { type = string }\n'
            f'resource "aws_s3_bucket" "main" {{ bucket = "${{var.environment}}-{bucket}" }}\n'
        )
        (p / "main.tf").write_text(content)
    m = root / "modules" / "tags"
    m.mkdir(parents=True)
    (m / "main.tf").write_text('variable "environment" { type = string }\noutput "env" { value = var.environment }\n')
    e = root / "etc"
    e.mkdir()
    (e / "env_eu-west-2_dev.tfvars").write_text('environment = "dev"\n')
    (e / "versions_eu-west-2_dev.tfvars").write_text('app_version = "1"\n')


def test_tfscaffold_discovery_and_namespacing(tmp_path: Path):
    make_repo(tmp_path)
    cfg = load(tmp_path)
    assert is_tfscaffold(tmp_path, cfg)
    sm = discover_tfscaffold(tmp_path, cfg)
    assert {u.name for u in sm.components} == {"network", "data"}
    assert {u.name for u in sm.modules} == {"tags"}
    assert sm.environments == {"dev"}
    assert sm.regions == {"eu-west-2"}

    r = runner.invoke(app, ["init", str(tmp_path)])
    assert r.exit_code == 0, r.output
    assert (tmp_path / ".okf/generated/components/network/resources/aws_s3_bucket.main.md").exists()
    assert (tmp_path / ".okf/generated/components/data/resources/aws_s3_bucket.main.md").exists()
    assert (tmp_path / ".okf/generated/shared-modules/tags/index.md").exists()
    assert (tmp_path / ".okf/generated/topology.md").exists()
    assert "dev" in (tmp_path / ".okf/generated/environments.md").read_text()
    copilot = (tmp_path / ".github/copilot-instructions.md").read_text()
    assert "tfscaffold" in copilot
    assert "independent root module/state boundary" in copilot

    r = runner.invoke(app, ["check", str(tmp_path)])
    assert r.exit_code == 0, r.output
    (tmp_path / "components/network/main.tf").write_text('resource "aws_s3_bucket" "main" { bucket = "changed" }\n')
    r = runner.invoke(app, ["check", str(tmp_path)])
    assert r.exit_code == 1
    assert "components/network" in r.output


def test_tfscaffold_component_description_survives_regeneration(tmp_path: Path):
    make_repo(tmp_path)
    cfg = load(tmp_path)
    model = discover_tfscaffold(tmp_path, cfg)
    out = tmp_path / ".okf"
    generate_tfscaffold_bundle(model, out, cfg)

    index = out / "generated" / "components" / "network" / "index.md"
    text = index.read_text()
    replacement = "This component manages the shared network boundary for application workloads."
    pattern = re.compile(
        r"<!-- tf2okf:manual-description-start -->\n.*?\n<!-- tf2okf:manual-description-end -->",
        re.S,
    )
    index.write_text(
        pattern.sub(
            f"<!-- tf2okf:manual-description-start -->\n{replacement}\n<!-- tf2okf:manual-description-end -->",
            text,
            count=1,
        )
    )

    generate_tfscaffold_bundle(model, out, cfg)
    assert replacement in index.read_text()


def test_tfscaffold_compact_profile_skips_resource_concepts(tmp_path: Path):
    make_repo(tmp_path)
    cfg = load(tmp_path)
    cfg["generation"]["profile"] = "compact"
    model = discover_tfscaffold(tmp_path, cfg)
    out = tmp_path / ".okf"
    generate_tfscaffold_bundle(model, out, cfg)
    assert not (out / "generated/components/network/resources").exists()
    inputs = (out / "generated/components/network/inputs.md").read_text()
    assert "| Name | Type | Required | Default |" in inputs
