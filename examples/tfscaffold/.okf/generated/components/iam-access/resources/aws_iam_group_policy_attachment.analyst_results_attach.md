---
type: Terraform Resource
title: aws_iam_group_policy_attachment.analyst_results_attach
description: Resource `aws_iam_group_policy_attachment.analyst_results_attach` in
  tfscaffold component `iam-access`.
tags:
- terraform
- tfscaffold
- component
- iam-access
- resource
- aws_iam_group_policy_attachment
generated:
  by: tf2okf/0.4.0
  at: '2026-09-19T10:27:39Z'
resource: terraform://tfscaffold/component/iam-access/aws_iam_group_policy_attachment.analyst_results_attach
sources:
- id: source-1
  resource: ../../../../../components/iam-access/main.tf
  author: process:terraform
---


# aws_iam_group_policy_attachment.analyst_results_attach

- tfscaffold Component: `iam-access`
- File: `components/iam-access/main.tf`
- Terraform address: `aws_iam_group_policy_attachment.analyst_results_attach`

## Configuration

| Attribute | Expression |
|---|---|
| `group` | `var.data_analyst_group_name` |
| `policy_arn` | `aws_iam_policy.athena_results_access.arn` |

## References

- `aws_iam_policy.athena_results_access.arn`
- `var.data_analyst_group_name`
