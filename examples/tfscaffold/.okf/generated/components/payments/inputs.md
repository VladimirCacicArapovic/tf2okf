---
type: Terraform Inputs
title: payments Inputs
description: Inputs for tfscaffold component `payments`.
tags:
- terraform
- tfscaffold
- component
- inputs
generated:
  by: tf2okf/0.4.0
  at: '2026-08-19T22:09:43Z'
sources:
- id: source-1
  resource: ../../../../components/payments/main.tf
  author: process:terraform
---


# payments Inputs

These inputs describe the values expected by this tfscaffold unit, including defaults and captured descriptions.

| Name | Type | Default | Sensitive | Description |
|---|---|---|---|---|
| `alb_security_group_id` | `string` | `required` | false | ALB security group id. |
| `app_security_group_id` | `string` | `required` | false | Application security group id. |
| `component_name` | `string` | `"payments"` | false | Logical payments component name. |
| `container_image` | `string` | `required` | false | Container image URI for payments. |
| `container_port` | `number` | `8443` | false | Container port for payments. |
| `environment` | `string` | `required` | false | Deployment environment for payments infrastructure. |
| `extra_tags` | `map(string)` | `{}` | false | Extra tags for payments resources. |
| `private_subnet_ids` | `list(string)` | `required` | false | Private subnets for payments ECS tasks. |
| `public_subnet_ids` | `list(string)` | `required` | false | Public subnets for payments ALB. |
| `region` | `string` | `required` | false | AWS region where payments is deployed. |
| `vpc_id` | `string` | `required` | false | VPC id for payments networking. |
