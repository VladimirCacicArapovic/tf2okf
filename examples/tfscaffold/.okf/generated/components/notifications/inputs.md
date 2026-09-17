---
type: Terraform Inputs
title: notifications Inputs
description: Inputs for tfscaffold component `notifications`.
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
  resource: ../../../../components/notifications/main.tf
  author: process:terraform
---


# notifications Inputs

These inputs describe the values expected by this tfscaffold unit, including defaults and captured descriptions.

| Name | Type | Default | Sensitive | Description |
|---|---|---|---|---|
| `alb_security_group_id` | `string` | `required` | false | ALB security group id. |
| `app_security_group_id` | `string` | `required` | false | Application security group id. |
| `component_name` | `string` | `"notifications"` | false | Logical notifications component name. |
| `container_image` | `string` | `required` | false | Container image URI for notifications. |
| `container_port` | `number` | `8090` | false | Container port for notifications. |
| `environment` | `string` | `required` | false | Deployment environment for notifications infrastructure. |
| `extra_tags` | `map(string)` | `{}` | false | Extra tags for notifications resources. |
| `private_subnet_ids` | `list(string)` | `required` | false | Private subnets for notifications ECS tasks. |
| `public_subnet_ids` | `list(string)` | `required` | false | Public subnets for notifications ALB. |
| `region` | `string` | `required` | false | AWS region where notifications is deployed. |
| `vpc_id` | `string` | `required` | false | VPC id for notifications networking. |
