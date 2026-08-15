from pathlib import Path
import yaml
from tf2okf.parser import parse_terraform
from tf2okf.generator import generate_bundle
from tf2okf.config import DEFAULT

def frontmatter(path: Path):
    text=path.read_text(); parts=text.split('---',2); return yaml.safe_load(parts[1])

def test_okf_v02_and_preserves_manual(tmp_path: Path):
    (tmp_path/'main.tf').write_text('resource "aws_s3_bucket" "raw" { bucket = "x" }')
    out=tmp_path/'.okf'
    generate_bundle(parse_terraform(tmp_path),out,DEFAULT)
    assert 'okf_version: "0.2"' in (out/'index.md').read_text()
    concept=next((out/'generated'/'resources').glob('*.md'))
    fm=frontmatter(concept)
    assert fm['type'] == 'Terraform Resource'
    assert fm['generated']['by'].startswith('tf2okf/')
    assert fm['sources']
    manual=out/'knowledge'/'architecture.md'
    manual.write_text('CUSTOM')
    generate_bundle(parse_terraform(tmp_path),out,DEFAULT)
    assert manual.read_text() == 'CUSTOM'

def test_resource_source_path_points_back_to_repo(tmp_path: Path):
    (tmp_path/'main.tf').write_text('resource "aws_s3_bucket" "raw" { bucket = "x" }')
    out=tmp_path/'.okf'
    generate_bundle(parse_terraform(tmp_path),out,DEFAULT)
    concept=next((out/'generated'/'resources').glob('*.md'))
    fm=frontmatter(concept)
    source=(concept.parent / fm['sources'][0]['resource']).resolve()
    assert source == (tmp_path/'main.tf').resolve()
