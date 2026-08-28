---
type: Terraform Module Call
title: module.ecs_service
description: Module call `ecs_service` from tfscaffold component `payments`.
tags:
- terraform
- tfscaffold
- component
- payments
- module-call
generated:
  by: tf2okf/0.4.0
  at: '2026-08-19T22:09:43Z'
resource: terraform://tfscaffold/component/payments/module.ecs_service
sources:
- id: source-1
  resource: ../../../../../components/payments/main.tf
  author: process:terraform
---


# module.ecs_service

- Source: `../../modules/ecs-service`
- Defined in: `components/payments/main.tf`

## References

- `local.effective_service_name`
- `local.payments_tags`
- `var.alb_security_group_id`
- `var.app_security_group_id`
- `var.container_image`
- `var.container_port`
- `var.environment`
- `var.private_subnet_ids`
- `var.public_subnet_ids`
- `var.vpc_id`
