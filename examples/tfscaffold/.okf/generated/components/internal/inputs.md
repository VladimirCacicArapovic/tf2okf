---
type: Terraform Inputs
title: internal Inputs
description: Inputs for tfscaffold component `internal`.
tags:
- terraform
- tfscaffold
- component
- inputs
generated:
  by: tf2okf/0.4.0
  at: '2026-09-19T10:27:39Z'
sources:
- id: source-1
  resource: ../../../../components/internal/main.tf
  author: process:terraform
---


# internal Inputs

These inputs describe the values expected by this tfscaffold unit, including defaults and captured descriptions.

| Name | Type | Default | Sensitive | Description |
|---|---|---|---|---|
| `component_name` | `string` | `"internal"` | false | Logical internal component name. |
| `environment` | `string` | `required` | false | Deployment environment for internal security infrastructure. |
| `extra_tags` | `map(string)` | `{}` | false | Extra tags for internal security resources. |
| `region` | `string` | `required` | false | AWS region where internal security is deployed. |
| `vpc_id` | `string` | `required` | false | VPC id where internal security groups are created. |
