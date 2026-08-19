from pathlib import Path

import yaml

from tf2okf.config import DEFAULT, load
from tf2okf.generator import generate_bundle
from tf2okf.parser import parse_terraform


def frontmatter(path: Path):
    text = path.read_text()
    parts = text.split("---", 2)
    return yaml.safe_load(parts[1])


def test_okf_v02_and_preserves_manual(tmp_path: Path):
    (tmp_path / "main.tf").write_text('resource "aws_s3_bucket" "raw" { bucket = "x" }')
    out = tmp_path / ".okf"
    generate_bundle(parse_terraform(tmp_path), out, DEFAULT)
    assert 'okf_version: "0.2"' in (out / "index.md").read_text()
    concept = next((out / "generated" / "resources").glob("*.md"))
    fm = frontmatter(concept)
    assert fm["type"] == "Terraform Resource"
    assert fm["generated"]["by"].startswith("tf2okf/")
    assert fm["sources"]
    manual = out / "knowledge" / "architecture.md"
    manual.write_text("CUSTOM")
    generate_bundle(parse_terraform(tmp_path), out, DEFAULT)
    assert manual.read_text() == "CUSTOM"


def test_resource_source_path_points_back_to_repo(tmp_path: Path):
    (tmp_path / "main.tf").write_text('resource "aws_s3_bucket" "raw" { bucket = "x" }')
    out = tmp_path / ".okf"
    generate_bundle(parse_terraform(tmp_path), out, DEFAULT)
    concept = next((out / "generated" / "resources").glob("*.md"))
    fm = frontmatter(concept)
    source = (concept.parent / fm["sources"][0]["resource"]).resolve()
    assert source == (tmp_path / "main.tf").resolve()


def test_compact_profile_reduces_surface_and_tables(tmp_path: Path):
    (tmp_path / "main.tf").write_text(
        'variable "env" { type = string }\n'
        'variable "password" {\n'
        '  type      = string\n'
        '  default   = "super-secret"\n'
        '  sensitive = true\n'
        '}\n'
        'resource "null_resource" "x" {}\n'
        'output "id" { value = null_resource.x.id }\n'
    )
    cfg = load(tmp_path)
    cfg["generation"]["profile"] = "compact"
    out = tmp_path / ".okf"
    generate_bundle(parse_terraform(tmp_path), out, cfg)
    assert not (out / "generated" / "resources").exists()
    text = (out / "generated" / "inputs.md").read_text()
    assert "| Name | Type | Required | Default |" in text
    assert "super-secret" not in text
