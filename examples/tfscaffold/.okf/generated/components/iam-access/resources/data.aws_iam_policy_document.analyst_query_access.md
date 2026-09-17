---
type: Terraform Data Source
title: data.aws_iam_policy_document.analyst_query_access
description: Data `data.aws_iam_policy_document.analyst_query_access` in tfscaffold
  component `iam-access`.
tags:
- terraform
- tfscaffold
- component
- iam-access
- data
- aws_iam_policy_document
generated:
  by: tf2okf/0.4.0
  at: '2026-09-17T19:58:26Z'
resource: terraform://tfscaffold/component/iam-access/data.aws_iam_policy_document.analyst_query_access
sources:
- id: source-1
  resource: ../../../../../components/iam-access/main.tf
  author: process:terraform
---


# data.aws_iam_policy_document.analyst_query_access

- tfscaffold Component: `iam-access`
- File: `components/iam-access/main.tf`
- Terraform address: `data.aws_iam_policy_document.analyst_query_access`

## Configuration

| Attribute | Expression |
|---|---|
| `actions` | `[
"glue:GetDatabase",
"glue:GetDatabases",
"glue:GetTable",
"glue:GetTables"
]` |
| `effect` | `"Allow"` |
| `resources` | `[
var.glue_catalog_arn,
local.glue_database_arn
]` |
| `sid` | `"GlueRead"` |

## References

- `local.athena_workgroup_arn`
- `local.glue_database_arn`
- `var.glue_catalog_arn`
