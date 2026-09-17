---
type: Terraform Outputs
title: iam-access Outputs
description: Outputs for tfscaffold component `iam-access`.
tags:
- terraform
- tfscaffold
- component
- outputs
generated:
  by: tf2okf/0.4.0
  at: '2026-09-17T19:58:26Z'
sources:
- id: source-1
  resource: ../../../../components/iam-access/main.tf
  author: process:terraform
---


# iam-access Outputs

These outputs summarize what this tfscaffold unit exposes to other components or operators.

| Name | Value | Sensitive | Description |
|---|---|---|---|
| `analyst_policy_document_json` | `data.aws_iam_policy_document.analyst_query_access.json` | false | Rendered IAM policy document for analyst Athena and Glue access. |
| `results_policy_arn` | `aws_iam_policy.athena_results_access.arn` | false | Managed IAM policy ARN attached to the analyst group. |
