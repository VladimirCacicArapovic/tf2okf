---
type: Terraform Inputs
title: checkout Inputs
description: Inputs for tfscaffold component `checkout`.
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
  resource: ../../../../components/checkout/main.tf
  author: process:terraform
---


# checkout Inputs

These inputs describe the values expected by this tfscaffold unit, including defaults and captured descriptions.

| Name | Type | Default | Sensitive | Description |
|---|---|---|---|---|
| `alb_security_group_id` | `string` | `required` | false | ALB security group id. |
| `app_security_group_id` | `string` | `required` | false | Application security group id. |
| `component_name` | `string` | `"checkout"` | false | Logical checkout component name. |
| `container_image` | `string` | `required` | false | Container image URI for checkout. |
| `container_port` | `number` | `8080` | false | Container port for checkout. |
| `desired_count` | `number` | `2` | false | Desired ECS task count for checkout. |
| `environment` | `string` | `required` | false | Deployment environment for checkout infrastructure. |
| `extra_tags` | `map(string)` | `{}` | false | Extra tags for checkout resources. |
| `private_subnet_ids` | `list(string)` | `required` | false | Private subnets for checkout ECS tasks. |
| `public_subnet_ids` | `list(string)` | `required` | false | Public subnets for checkout ALB. |
| `region` | `string` | `required` | false | AWS region where checkout is deployed. |
| `service_name_override` | `string` | `""` | false | Optional explicit ECS service name. |
| `vpc_id` | `string` | `required` | false | VPC id for checkout networking. |
