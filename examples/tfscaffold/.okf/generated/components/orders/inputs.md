---
type: Terraform Inputs
title: orders Inputs
description: Inputs for tfscaffold component `orders`.
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
  resource: ../../../../components/orders/main.tf
  author: process:terraform
---


# orders Inputs

These inputs describe the values expected by this tfscaffold unit, including defaults and captured descriptions.

| Name | Type | Default | Sensitive | Description |
|---|---|---|---|---|
| `alb_security_group_id` | `string` | `required` | false | ALB security group id. |
| `app_security_group_id` | `string` | `required` | false | Application security group id. |
| `component_name` | `string` | `"orders"` | false | Logical orders component name. |
| `container_image` | `string` | `required` | false | Container image URI for orders. |
| `container_port` | `number` | `8081` | false | Container port for orders. |
| `environment` | `string` | `required` | false | Deployment environment for orders infrastructure. |
| `extra_tags` | `map(string)` | `{}` | false | Extra tags for orders resources. |
| `private_subnet_ids` | `list(string)` | `required` | false | Private subnets for orders ECS tasks. |
| `public_subnet_ids` | `list(string)` | `required` | false | Public subnets for orders ALB. |
| `region` | `string` | `required` | false | AWS region where orders is deployed. |
| `vpc_id` | `string` | `required` | false | VPC id for orders networking. |
