from pathlib import Path

import yaml

from tf2okf.config import load
from tf2okf.generator import generate_bundle
from tf2okf.parser import parse_terraform


def _frontmatter(text: str):
    assert text.startswith("---\n")
    _, fm, _ = text.split("---", 2)
    return yaml.safe_load(fm)


def test_generated_concepts_have_required_type(tmp_path: Path):
    (tmp_path / "main.tf").write_text(
        'variable "env" { type = string }\nresource "null_resource" "x" {}\noutput "id" { value = null_resource.x.id }\n'
    )
    generate_bundle(parse_terraform(tmp_path), tmp_path / ".okf", load(tmp_path))
    for p in (tmp_path / ".okf/generated").rglob("*.md"):
        if p.name == "index.md":
            continue
        assert _frontmatter(p.read_text())["type"]
    assert 'okf_version: "0.2"' in (tmp_path / ".okf/index.md").read_text()


def test_manual_knowledge_survives_regeneration(tmp_path: Path):
    (tmp_path / "main.tf").write_text('resource "null_resource" "x" {}')
    cfg = load(tmp_path)
    out = tmp_path / ".okf"
    generate_bundle(parse_terraform(tmp_path), out, cfg)
    marker = "\nHuman decision: do not destroy this.\n"
    p = out / "knowledge/architecture.md"
    p.write_text(p.read_text() + marker)
    generate_bundle(parse_terraform(tmp_path), out, cfg)
    assert marker.strip() in p.read_text()
