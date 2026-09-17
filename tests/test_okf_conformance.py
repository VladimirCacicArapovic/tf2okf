from pathlib import Path

import yaml

from tf2okf.config import load
from tf2okf.generator import generate_bundle
from tf2okf.parser import parse_terraform
from tf2okf.scaffold import discover_tfscaffold
from tf2okf.scaffold_generator import generate_tfscaffold_bundle


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


def test_extended_curated_knowledge_files_are_created(tmp_path: Path):
    (tmp_path / "main.tf").write_text('resource "null_resource" "x" {}')
    cfg = load(tmp_path)
    out = tmp_path / ".okf"
    generate_bundle(parse_terraform(tmp_path), out, cfg)

    for rel in [
        "knowledge/architecture.md",
        "knowledge/security.md",
        "knowledge/task-routing.md",
        "knowledge/iam-permissions.md",
        "knowledge/aws-advisories.md",
    ]:
        assert (out / rel).exists(), rel

    root_index = (out / "index.md").read_text()
    assert "knowledge/task-routing.md" in root_index
    assert "knowledge/iam-permissions.md" in root_index
    assert "knowledge/aws-advisories.md" in root_index


def test_iam_policy_document_actions_are_extracted(tmp_path: Path):
    (tmp_path / "main.tf").write_text(
        '''
        data "aws_iam_policy_document" "athena_access" {
          statement {
            sid     = "AthenaQuery"
            effect  = "Allow"
            actions = ["athena:StartQueryExecution", "athena:GetQueryExecution"]
            resources = ["*"]
          }
        }
        '''
    )

    model = parse_terraform(tmp_path)

    assert len(model.iam_policies) == 1
    fact = model.iam_policies[0]
    assert fact.address == "data.aws_iam_policy_document.athena_access"
    assert len(fact.statements) == 1
    assert fact.statements[0].sid == "AthenaQuery"
    assert fact.statements[0].actions == ["athena:StartQueryExecution", "athena:GetQueryExecution"]
    assert fact.statements[0].resources == ["*"]


def test_iam_access_page_is_generated(tmp_path: Path):
    (tmp_path / "main.tf").write_text(
        '''
        data "aws_iam_policy_document" "glue_access" {
          statement {
            sid     = "GlueRead"
            effect  = "Allow"
            actions = ["glue:GetDatabase", "glue:GetTable"]
            resources = ["*"]
          }
        }

        resource "aws_iam_group_policy_attachment" "analyst_attach" {
          group      = "data-analyst-team"
          policy_arn = data.aws_iam_policy_document.glue_access.json
        }
        '''
    )
    cfg = load(tmp_path)
    out = tmp_path / ".okf"

    generate_bundle(parse_terraform(tmp_path), out, cfg)

    iam_page = (out / "generated/iam-access.md").read_text()
    index_page = (out / "generated/index.md").read_text()
    assert "GlueRead" in iam_page
    assert "glue:GetDatabase, glue:GetTable" in iam_page
    assert "group:data-analyst-team" in iam_page
    assert "iam-access.md" in index_page


def test_inline_iam_policy_jsonencode_is_extracted(tmp_path: Path):
    (tmp_path / "main.tf").write_text(
        '''
        resource "aws_iam_policy" "athena_runtime" {
          name = "athena-runtime"
          policy = jsonencode({
            Version = "2012-10-17"
            Statement = [
              {
                Sid = "AthenaApi"
                Effect = "Allow"
                Action = ["athena:ListWorkGroups", "athena:GetWorkGroup"]
                Resource = ["*"]
              },
              {
                Sid = "GlueCatalog"
                Effect = "Allow"
                Action = "glue:GetDatabases"
                Resource = "*"
                Principal = {
                  Service = "athena.amazonaws.com"
                }
              }
            ]
          })
        }
        '''
    )

    model = parse_terraform(tmp_path)

    assert len(model.iam_policies) == 1
    fact = model.iam_policies[0]
    assert fact.address == "aws_iam_policy.athena_runtime"
    assert [statement.sid for statement in fact.statements] == ["AthenaApi", "GlueCatalog"]
    assert fact.statements[0].actions == ["athena:ListWorkGroups", "athena:GetWorkGroup"]
    assert fact.statements[1].actions == ["glue:GetDatabases"]
    assert fact.statements[1].principals == ["Service:athena.amazonaws.com"]


def test_tfscaffold_unit_gets_iam_access_page(tmp_path: Path):
    (tmp_path / "bin").mkdir()
    (tmp_path / "bin/terraform.sh").write_text("#!/bin/sh\n")
    (tmp_path / "components").mkdir()
    (tmp_path / "modules").mkdir()
    component = tmp_path / "components/analytics"
    component.mkdir()
    (component / "main.tf").write_text(
        '''
        data "aws_iam_policy_document" "query_access" {
          statement {
            sid     = "AthenaQuery"
            effect  = "Allow"
            actions = ["athena:StartQueryExecution"]
            resources = ["*"]
          }
        }
        '''
    )

    cfg = load(tmp_path)
    out = tmp_path / ".okf"
    model = discover_tfscaffold(tmp_path, cfg)
    generate_tfscaffold_bundle(model, out, cfg)

    unit_index = (out / "generated/components/analytics/index.md").read_text()
    iam_page = (out / "generated/components/analytics/iam-access.md").read_text()
    assert "IAM access" in unit_index
    assert "AthenaQuery" in iam_page
    assert "athena:StartQueryExecution" in iam_page
