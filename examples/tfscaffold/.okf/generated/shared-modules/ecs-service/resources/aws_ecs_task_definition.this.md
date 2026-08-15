---
type: Terraform Resource
title: aws_ecs_task_definition.this
description: Resource `aws_ecs_task_definition.this` in tfscaffold module `ecs-service`.
tags:
- terraform
- tfscaffold
- module
- ecs-service
- resource
- aws_ecs_task_definition
generated:
  by: tf2okf/0.4.0
  at: '2026-08-15T09:33:39Z'
resource: terraform://tfscaffold/module/ecs-service/aws_ecs_task_definition.this
sources:
- id: source-1
  resource: ../../../../../modules/ecs-service/main.tf
  author: process:terraform
---


# aws_ecs_task_definition.this

- tfscaffold Module: `ecs-service`
- File: `modules/ecs-service/main.tf`
- Terraform address: `aws_ecs_task_definition.this`

## Configuration

| Attribute | Expression |
|---|---|
| `container_definitions` | `jsonencode([` |
| `cpu` | `"256"` |
| `family` | `"${var.environment}-${var.app_name}"` |
| `memory` | `"512"` |
| `network_mode` | `"awsvpc"` |
| `requires_compatibilities` | `["FARGATE"]` |
| `tags` | `merge(var.tags, {` |

## References

- `var.app_name`
- `var.container_image`
- `var.container_port`
- `var.environment`
- `var.tags`
