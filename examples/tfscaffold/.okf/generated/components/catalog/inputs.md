---
type: Terraform Inputs
title: catalog Inputs
description: Inputs for tfscaffold component `catalog`.
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
  resource: ../../../../components/catalog/main.tf
  author: process:terraform
---


# catalog Inputs

These inputs describe the values expected by this tfscaffold unit, including defaults and captured descriptions.

| Name | Type | Default | Sensitive | Description |
|---|---|---|---|---|
| `alb_security_group_id` | `string` | `required` | false | ALB security group id. |
| `app_security_group_id` | `string` | `required` | false | Application security group id. |
| `component_name` | `string` | `"catalog"` | false | Logical catalog component name. |
| `container_image` | `string` | `required` | false | Container image URI for catalog. |
| `container_port` | `number` | `8080` | false | Container port for catalog. |
| `environment` | `string` | `required` | false | Deployment environment for catalog infrastructure. |
| `extra_tags` | `map(string)` | `{}` | false | Extra tags for catalog resources. |
| `private_subnet_ids` | `list(string)` | `required` | false | Private subnets for catalog ECS tasks. |
| `public_subnet_ids` | `list(string)` | `required` | false | Public subnets for catalog ALB. |
| `region` | `string` | `required` | false | AWS region where catalog is deployed. |
| `service_name_override` | `string` | `""` | false | Optional explicit ECS service name. |
| `vpc_id` | `string` | `required` | false | VPC id for catalog networking. |
