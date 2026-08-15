---
type: Terraform Resource
title: aws_lb.this
description: Resource `aws_lb.this` in tfscaffold module `ecs-service`.
tags:
- terraform
- tfscaffold
- module
- ecs-service
- resource
- aws_lb
generated:
  by: tf2okf/0.4.0
  at: '2026-08-15T09:33:39Z'
resource: terraform://tfscaffold/module/ecs-service/aws_lb.this
sources:
- id: source-1
  resource: ../../../../../modules/ecs-service/main.tf
  author: process:terraform
---


# aws_lb.this

- tfscaffold Module: `ecs-service`
- File: `modules/ecs-service/main.tf`
- Terraform address: `aws_lb.this`

## Configuration

| Attribute | Expression |
|---|---|
| `internal` | `false` |
| `load_balancer_type` | `"application"` |
| `name` | `substr("${var.environment}-${var.app_name}-alb", 0, 32)` |
| `security_groups` | `[var.alb_security_group_id]` |
| `subnets` | `var.public_subnet_ids` |
| `tags` | `merge(var.tags, {` |

## References

- `var.alb_security_group_id`
- `var.app_name`
- `var.environment`
- `var.public_subnet_ids`
- `var.tags`
