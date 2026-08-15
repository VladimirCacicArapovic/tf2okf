---
type: Terraform Resource
title: aws_ecs_service.this
description: Resource `aws_ecs_service.this` in tfscaffold module `ecs-service`.
tags:
- terraform
- tfscaffold
- module
- ecs-service
- resource
- aws_ecs_service
generated:
  by: tf2okf/0.4.0
  at: '2026-08-15T09:33:39Z'
resource: terraform://tfscaffold/module/ecs-service/aws_ecs_service.this
sources:
- id: source-1
  resource: ../../../../../modules/ecs-service/main.tf
  author: process:terraform
---


# aws_ecs_service.this

- tfscaffold Module: `ecs-service`
- File: `modules/ecs-service/main.tf`
- Terraform address: `aws_ecs_service.this`

## Configuration

| Attribute | Expression |
|---|---|
| `cluster` | `aws_ecs_cluster.this.id` |
| `depends_on` | `[aws_lb_listener.http]` |
| `desired_count` | `2` |
| `launch_type` | `"FARGATE"` |
| `name` | `"${var.environment}-${var.app_name}"` |
| `tags` | `merge(var.tags, {` |
| `task_definition` | `aws_ecs_task_definition.this.arn` |

## References

- `aws_ecs_cluster.this.id`
- `aws_ecs_task_definition.this.arn`
- `aws_lb_listener.http`
- `aws_lb_target_group.this.arn`
- `var.app_name`
- `var.app_security_group_id`
- `var.container_port`
- `var.environment`
- `var.private_subnet_ids`
- `var.tags`
