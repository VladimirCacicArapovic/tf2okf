from pathlib import Path
from tf2okf.parser import parse_terraform

def test_parser_extracts_core_blocks(tmp_path: Path):
    (tmp_path/'main.tf').write_text('''
variable "env" { type = string }
resource "aws_s3_bucket" "raw" { bucket = "${var.env}-raw" }
resource "aws_s3_bucket_versioning" "raw" { bucket = aws_s3_bucket.raw.id }
module "net" { source = "./net" env = var.env }
output "bucket" { value = aws_s3_bucket.raw.bucket }
''')
    m=parse_terraform(tmp_path)
    assert {r.address for r in m.resources} == {'aws_s3_bucket.raw','aws_s3_bucket_versioning.raw'}
    assert m.modules[0].name == 'net'
    assert m.variables[0].name == 'env'
    assert m.outputs[0].name == 'bucket'
    assert 'aws_s3_bucket.raw.id' in m.resources[1].references

def test_terraform_docs_enrichment(tmp_path: Path):
    from tf2okf.parser import enrich_from_terraform_docs
    (tmp_path/'main.tf').write_text('''
variable "env" {\n  type = string\n}\noutput "name" {\n  value = var.env\n}\n''')
    m=parse_terraform(tmp_path)
    enrich_from_terraform_docs(m, {
        'inputs': [{'name':'env','type':'string','description':'Environment name','required':True}],
        'outputs': [{'name':'name','description':'Selected environment'}]
    })
    assert m.variables[0].description == 'Environment name'
    assert m.outputs[0].description == 'Selected environment'
