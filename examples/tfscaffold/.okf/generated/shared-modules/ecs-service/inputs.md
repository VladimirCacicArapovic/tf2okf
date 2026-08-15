---
type: Terraform Inputs
title: ecs-service Inputs
description: Inputs for tfscaffold module `ecs-service`.
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
  resource: ../../../../modules/ecs-service/main.tf
  author: process:terraform
---


# ecs-service Inputs

These inputs describe the values expected by this tfscaffold unit, including defaults and captured descriptions.

| Name | Type | Default | Sensitive | Description |
|---|---|---|---|---|
| `alb_security_group_id` | `string` | `required` | false | Security group identifier attached to the application load balancer. |
| `app_name` | `string` | `required` | false | Logical application name used across ECS service resources. |
| `app_security_group_id` | `string` | `required` | false | Security group identifier attached to ECS service tasks. |
| `container_image` | `string` | `required` | false | Container image URI deployed to the ECS task definition. |
| `container_port` | `number` | `required` | false | Container port exposed by the application workload. |
| `environment` | `string` | `required` | false | Deployment environment used for naming ECS and ALB resources. |
| `private_subnet_ids` | `list(string)` | `required` | false | Private subnet identifiers used for ECS task networking. |
| `public_subnet_ids` | `list(string)` | `required` | false | Public subnet identifiers used by the internet-facing ALB. |
| `tags` | `map(string)` | `required` | false | Common tags applied to ECS, load balancer, and target group resources. |
| `vpc_id` | `string` | `required` | false | Identifier of the VPC hosting the ECS service and load balancer. |
