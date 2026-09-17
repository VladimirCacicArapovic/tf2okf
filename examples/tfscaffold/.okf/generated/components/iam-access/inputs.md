---
type: Terraform Inputs
title: iam-access Inputs
description: Inputs for tfscaffold component `iam-access`.
tags:
- terraform
- tfscaffold
- component
- inputs
generated:
  by: tf2okf/0.4.0
  at: '2026-09-17T19:58:26Z'
sources:
- id: source-1
  resource: ../../../../components/iam-access/main.tf
  author: process:terraform
---


# iam-access Inputs

These inputs describe the values expected by this tfscaffold unit, including defaults and captured descriptions.

| Name | Type | Default | Sensitive | Description |
|---|---|---|---|---|
| `analytics_bucket_arn` | `string` | `"arn:aws:s3:::example-analytics-results"` | false | S3 bucket ARN used by analytics principals for Athena query results. |
| `data_analyst_group_name` | `string` | `"data-analyst-team"` | false | IAM group representing analyst users. |
| `environment` | `string` | `required` | false | Deployment environment for IAM access examples. |
| `glue_catalog_arn` | `string` | `"arn:aws:glue:eu-west-2:123456789012:catalog"` | false | Glue catalog ARN used by analytics principals. |
| `region` | `string` | `required` | false | AWS region where IAM access examples are evaluated. |
