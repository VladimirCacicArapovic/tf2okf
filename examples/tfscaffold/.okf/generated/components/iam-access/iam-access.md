---
type: IAM Access Summary
title: iam-access IAM Access
description: Extracted IAM policy actions, resources, and attachment hints for tfscaffold
  component `iam-access`.
tags:
- terraform
- tfscaffold
- component
- iam-access
- iam
- access
generated:
  by: tf2okf/0.4.0
  at: '2026-09-19T10:27:39Z'
sources:
- id: source-1
  resource: ../../../../components/iam-access/main.tf
  author: process:terraform
---


# iam-access IAM Access

This page summarizes IAM policy facts extracted from this tfscaffold unit. It is source-only and best-effort, so treat Terraform as the source of truth for merged or computed policies.

## `aws_iam_policy.athena_results_access`

- File: `components/iam-access/main.tf`
- Attachments: `group:var.data_analyst_group_name`
- Raw policy expression: `jsonencode({
Version = "2012-10-17"
Statement = [
{
Sid      = "AthenaResultsBucket"
Effect   = "Allow"
Action   = ["s3:GetObject", "s3:PutObject"]
Resource = ["${var.analytics_bucket_arn}/*"]
}
]
})`

| Sid | Effect | Actions | Resources | Principals |
|---|---|---|---|---|
| `AthenaResultsBucket` | `Allow` | `s3:GetObject, s3:PutObject` | `${var.analytics_bucket_arn}/*` | `` |

## `data.aws_iam_policy_document.analyst_query_access`

- File: `components/iam-access/main.tf`

| Sid | Effect | Actions | Resources | Principals |
|---|---|---|---|---|
| `AthenaQuery` | `Allow` | `athena:GetQueryExecution, athena:GetQueryResults, athena:ListWorkGroups, athena:StartQueryExecution` | `*` | `` |
| `GlueRead` | `Allow` | `glue:GetDatabase, glue:GetDatabases, glue:GetTable, glue:GetTables` | `` | `` |
