---
type: Terraform Inputs
title: app Inputs
description: Inputs for tfscaffold component `app`.
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
  resource: ../../../../components/app/main.tf
  author: process:terraform
---


# app Inputs

These inputs describe the values expected by this tfscaffold unit, including defaults and captured descriptions.

| Name | Type | Default | Sensitive | Description |
|---|---|---|---|---|
| `alb_security_group_id` | `string` | `required` | false | Security group identifier attached to the application load balancer. |
| `app_name` | `string` | `required` | false | Logical application name used for ECS, ALB, and related resources. |
| `app_security_group_id` | `string` | `required` | false | Security group identifier attached to ECS tasks. |
| `container_image` | `string` | `required` | false | Container image URI deployed into the ECS service. |
| `container_port` | `number` | `required` | false | Application port exposed by the running container. |
| `environment` | `string` | `required` | false | Deployment environment name used in resource naming and tagging. |
| `private_subnet_ids` | `list(string)` | `required` | false | Private subnet identifiers used by the ECS service tasks. |
| `public_subnet_ids` | `list(string)` | `required` | false | Public subnet identifiers used by the internet-facing ALB. |
| `region` | `string` | `required` | false | AWS region where the application stack is provisioned. |
| `vpc_id` | `string` | `required` | false | Identifier of the VPC hosting the load balancer and ECS service. |
