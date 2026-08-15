---
type: Terraform Module Call
title: module.ecs_service
description: Module call `ecs_service` from tfscaffold component `app`.
tags:
- terraform
- tfscaffold
- component
- app
- module-call
generated:
  by: tf2okf/0.4.0
  at: '2026-08-15T09:33:39Z'
resource: terraform://tfscaffold/component/app/module.ecs_service
sources:
- id: source-1
  resource: ../../../../../components/app/main.tf
  author: process:terraform
---


# module.ecs_service

- Source: `../../modules/ecs-service`
- Defined in: `components/app/main.tf`

## References

- `module.tags.tags`
- `var.alb_security_group_id`
- `var.app_name`
- `var.app_security_group_id`
- `var.container_image`
- `var.container_port`
- `var.environment`
- `var.private_subnet_ids`
- `var.public_subnet_ids`
- `var.vpc_id`
