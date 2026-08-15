---
type: Terraform Inputs
title: security-groups Inputs
description: Inputs for tfscaffold module `security-groups`.
tags:
- terraform
- tfscaffold
- module
- inputs
generated:
  by: tf2okf/0.4.0
  at: '2026-08-15T09:33:39Z'
sources:
- id: source-1
  resource: ../../../../modules/security-groups/main.tf
  author: process:terraform
---


# security-groups Inputs

These inputs describe the values expected by this tfscaffold unit, including defaults and captured descriptions.

| Name | Type | Default | Sensitive | Description |
|---|---|---|---|---|
| `environment` | `string` | `required` | false | Deployment environment used for naming the security groups. |
| `tags` | `map(string)` | `required` | false | Common tags applied to security group resources. |
| `vpc_id` | `string` | `required` | false | Identifier of the VPC where security groups are created. |
