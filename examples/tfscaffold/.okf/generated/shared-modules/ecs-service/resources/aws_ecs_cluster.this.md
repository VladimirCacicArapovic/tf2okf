---
type: Terraform Resource
title: aws_ecs_cluster.this
description: Resource `aws_ecs_cluster.this` in tfscaffold module `ecs-service`.
tags:
- terraform
- tfscaffold
- module
- ecs-service
- resource
- aws_ecs_cluster
generated:
  by: tf2okf/0.4.0
  at: '2026-08-15T09:33:39Z'
resource: terraform://tfscaffold/module/ecs-service/aws_ecs_cluster.this
sources:
- id: source-1
  resource: ../../../../../modules/ecs-service/main.tf
  author: process:terraform
---


# aws_ecs_cluster.this

- tfscaffold Module: `ecs-service`
- File: `modules/ecs-service/main.tf`
- Terraform address: `aws_ecs_cluster.this`

## Configuration

| Attribute | Expression |
|---|---|
| `name` | `"${var.environment}-${var.app_name}"` |
| `tags` | `merge(var.tags, {` |

## References

- `var.app_name`
- `var.environment`
- `var.tags`
