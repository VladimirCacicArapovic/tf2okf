from pathlib import Path

from typer.testing import CliRunner

from tf2okf.cli import app

runner = CliRunner()


def test_init_generate_check_and_drift(tmp_path: Path):
    (tmp_path / "main.tf").write_text('resource "aws_s3_bucket" "raw" { bucket = "x" }')
    r = runner.invoke(app, ["init", str(tmp_path)])
    assert r.exit_code == 0, r.output
    r = runner.invoke(app, ["check", str(tmp_path)])
    assert r.exit_code == 0, r.output
    (tmp_path / "main.tf").write_text('resource "aws_s3_bucket" "raw" { bucket = "y" }')
    r = runner.invoke(app, ["check", str(tmp_path)])
    assert r.exit_code == 1
    assert "drift" in r.output.lower()


def test_generate_compact_profile(tmp_path: Path):
    (tmp_path / "main.tf").write_text(
        'variable "env" { type = string }\n'
        'resource "null_resource" "x" {}\n'
        'output "id" { value = null_resource.x.id }\n'
    )
    r = runner.invoke(app, ["generate", str(tmp_path), "--profile", "compact"])
    assert r.exit_code == 0, r.output
    assert "Profile: compact." in r.output
    assert not (tmp_path / ".okf/generated/resources").exists()


def test_check_ignores_generated_ai_directory(tmp_path: Path):
    (tmp_path / "main.tf").write_text('resource "null_resource" "x" {}')
    r = runner.invoke(app, ["init", str(tmp_path)])
    assert r.exit_code == 0, r.output
    ai = tmp_path / ".okf/generated/ai/overview.md"
    ai.parent.mkdir(parents=True, exist_ok=True)
    ai.write_text("# AI Overview\n\nSynthetic content.\n")
    r = runner.invoke(app, ["check", str(tmp_path)])
    assert r.exit_code == 0, r.output
