---
type: Terraform Resource
title: aws_lb_target_group.this
description: Resource `aws_lb_target_group.this` in tfscaffold module `ecs-service`.
tags:
- terraform
- tfscaffold
- module
- ecs-service
- resource
- aws_lb_target_group
generated:
  by: tf2okf/0.4.0
  at: '2026-09-19T10:27:39Z'
resource: terraform://tfscaffold/module/ecs-service/aws_lb_target_group.this
sources:
- id: source-1
  resource: ../../../../../modules/ecs-service/main.tf
  author: process:terraform
---


# aws_lb_target_group.this

- tfscaffold Module: `ecs-service`
- File: `modules/ecs-service/main.tf`
- Terraform address: `aws_lb_target_group.this`

## Configuration

| Attribute | Expression |
|---|---|
| `name` | `substr("${var.environment}-${var.app_name}-tg", 0, 32)` |
| `path` | `"/health"` |
| `port` | `var.container_port` |
| `protocol` | `"HTTP"` |
| `tags` | `merge(var.tags, {
Name = "${var.environment}-${var.app_name}-tg"
})` |
| `target_type` | `"ip"` |
| `vpc_id` | `var.vpc_id` |

## References

- `var.app_name`
- `var.container_port`
- `var.environment`
- `var.tags`
- `var.vpc_id`
