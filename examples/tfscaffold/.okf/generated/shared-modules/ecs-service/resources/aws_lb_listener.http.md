---
type: Terraform Resource
title: aws_lb_listener.http
description: Resource `aws_lb_listener.http` in tfscaffold module `ecs-service`.
tags:
- terraform
- tfscaffold
- module
- ecs-service
- resource
- aws_lb_listener
generated:
  by: tf2okf/0.4.0
  at: '2026-08-15T09:33:39Z'
resource: terraform://tfscaffold/module/ecs-service/aws_lb_listener.http
sources:
- id: source-1
  resource: ../../../../../modules/ecs-service/main.tf
  author: process:terraform
---


# aws_lb_listener.http

- tfscaffold Module: `ecs-service`
- File: `modules/ecs-service/main.tf`
- Terraform address: `aws_lb_listener.http`

## Configuration

| Attribute | Expression |
|---|---|
| `load_balancer_arn` | `aws_lb.this.arn` |
| `port` | `80` |
| `protocol` | `"HTTP"` |

## References

- `aws_lb.this.arn`
- `aws_lb_target_group.this.arn`
