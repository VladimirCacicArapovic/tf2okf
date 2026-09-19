---
type: Terraform Resource
title: aws_iam_policy.athena_results_access
description: Resource `aws_iam_policy.athena_results_access` in tfscaffold component
  `iam-access`.
tags:
- terraform
- tfscaffold
- component
- iam-access
- resource
- aws_iam_policy
generated:
  by: tf2okf/0.4.0
  at: '2026-09-19T10:27:39Z'
resource: terraform://tfscaffold/component/iam-access/aws_iam_policy.athena_results_access
sources:
- id: source-1
  resource: ../../../../../components/iam-access/main.tf
  author: process:terraform
---


# aws_iam_policy.athena_results_access

- tfscaffold Component: `iam-access`
- File: `components/iam-access/main.tf`
- Terraform address: `aws_iam_policy.athena_results_access`

## Configuration

| Attribute | Expression |
|---|---|
| `name` | `"${var.environment}-athena-results-access"` |
| `policy` | `jsonencode({
Version = "2012-10-17"
Statement = [
{
Sid      = "AthenaResultsBucket"
Effect   = "Allow"
Action   = ["s3:GetObject", "s3:PutObject"]
Resource = ["${var.analytics_bucket_arn}/*"]
}
]
})` |

## References

- `var.analytics_bucket_arn`
- `var.environment`
