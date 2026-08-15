from pathlib import Path
from typer.testing import CliRunner
from tf2okf.cli import app

runner=CliRunner()

def test_init_generate_check_and_drift(tmp_path: Path):
    (tmp_path/'main.tf').write_text('resource "aws_s3_bucket" "raw" { bucket = "x" }')
    r=runner.invoke(app,['init',str(tmp_path)])
    assert r.exit_code == 0, r.output
    r=runner.invoke(app,['check',str(tmp_path)])
    assert r.exit_code == 0, r.output
    (tmp_path/'main.tf').write_text('resource "aws_s3_bucket" "raw" { bucket = "y" }')
    r=runner.invoke(app,['check',str(tmp_path)])
    assert r.exit_code == 1
    assert 'drift' in r.output.lower()
