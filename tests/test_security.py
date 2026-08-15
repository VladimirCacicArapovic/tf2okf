from pathlib import Path
import pytest
from tf2okf.config import load
from tf2okf.parser import parse_terraform
from tf2okf.generator import generate_bundle
from tf2okf.security import SecurityError, redact_attribute


def test_output_path_cannot_escape_repo(tmp_path: Path):
    (tmp_path/'.tf2okf.yml').write_text('output:\n  directory: ../../outside\n')
    with pytest.raises(SecurityError): load(tmp_path)


def test_absolute_output_path_rejected(tmp_path: Path):
    (tmp_path/'.tf2okf.yml').write_text('output:\n  directory: /tmp/outside\n')
    with pytest.raises(SecurityError): load(tmp_path)


def test_terraform_root_cannot_escape_repo(tmp_path: Path):
    (tmp_path/'.tf2okf.yml').write_text('terraform:\n  root: ../outside\n')
    with pytest.raises(SecurityError): load(tmp_path)


def test_symlinked_terraform_is_ignored(tmp_path: Path):
    outside=tmp_path.parent/'outside-secret.tf'; outside.write_text('resource "x" "outside" {}')
    try: (tmp_path/'linked.tf').symlink_to(outside)
    except OSError: pytest.skip('symlink unsupported')
    (tmp_path/'main.tf').write_text('resource "x" "inside" {}')
    model=parse_terraform(tmp_path)
    assert [r.name for r in model.resources] == ['inside']


def test_secret_attributes_redacted_in_generated_markdown(tmp_path: Path):
    (tmp_path/'main.tf').write_text('resource "example" "x" {\n password = "super-secret"\n api_key = "abc123"\n name = "safe"\n}\n')
    model=parse_terraform(tmp_path)
    generate_bundle(model,tmp_path/'.okf',load(tmp_path))
    text=(tmp_path/'.okf/generated/resources/example.x.md').read_text()
    assert 'super-secret' not in text and 'abc123' not in text
    assert '<redacted-sensitive-value>' in text and 'safe' in text


def test_redaction_key_matching():
    assert redact_attribute('client_secret','x') == '<redacted-sensitive-value>'
    assert redact_attribute('name','x') == 'x'
