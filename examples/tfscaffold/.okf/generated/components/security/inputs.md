---
type: Terraform Inputs
title: security Inputs
description: Inputs for tfscaffold component `security`.
tags:
- terraform
- tfscaffold
- component
- inputs
generated:
  by: tf2okf/0.4.0
  at: '2026-08-15T09:33:39Z'
sources:
- id: source-1
  resource: ../../../../components/security/main.tf
  author: process:terraform
---


# security Inputs

These inputs describe the values expected by this tfscaffold unit, including defaults and captured descriptions.

| Name | Type | Default | Sensitive | Description |
|---|---|---|---|---|
| `environment` | `string` | `required` | false | Deployment environment name used in resource naming and tagging. |
| `region` | `string` | `required` | false | AWS region where security resources are provisioned. |
| `vpc_id` | `string` | `required` | false | Identifier of the VPC where security groups should be created. |
