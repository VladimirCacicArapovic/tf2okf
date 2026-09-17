---
type: Terraform Inputs
title: observability Inputs
description: Inputs for tfscaffold component `observability`.
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
  resource: ../../../../components/observability/main.tf
  author: process:terraform
---


# observability Inputs

These inputs describe the values expected by this tfscaffold unit, including defaults and captured descriptions.

| Name | Type | Default | Sensitive | Description |
|---|---|---|---|---|
| `alb_security_group_id` | `string` | `required` | false | ALB security group id. |
| `app_security_group_id` | `string` | `required` | false | Application security group id. |
| `component_name` | `string` | `"observability"` | false | Logical observability component name. |
| `container_image` | `string` | `required` | false | Container image URI for observability collector. |
| `container_port` | `number` | `4318` | false | Container port for observability collector. |
| `environment` | `string` | `required` | false | Deployment environment for observability infrastructure. |
| `extra_tags` | `map(string)` | `{}` | false | Extra tags for observability resources. |
| `private_subnet_ids` | `list(string)` | `required` | false | Private subnets for observability ECS tasks. |
| `public_subnet_ids` | `list(string)` | `required` | false | Public subnets for observability ALB. |
| `region` | `string` | `required` | false | AWS region where observability is deployed. |
| `vpc_id` | `string` | `required` | false | VPC id for observability networking. |
