---
type: Terraform Resource
title: aws_security_group.app
description: Resource `aws_security_group.app` in tfscaffold module `security-groups`.
tags:
- terraform
- tfscaffold
- module
- security-groups
- resource
- aws_security_group
generated:
  by: tf2okf/0.4.0
  at: '2026-08-15T09:33:39Z'
resource: terraform://tfscaffold/module/security-groups/aws_security_group.app
sources:
- id: source-1
  resource: ../../../../../modules/security-groups/main.tf
  author: process:terraform
---


# aws_security_group.app

- tfscaffold Module: `security-groups`
- File: `modules/security-groups/main.tf`
- Terraform address: `aws_security_group.app`

## Configuration

| Attribute | Expression |
|---|---|
| `description` | `"Allow traffic from the ALB to ECS tasks"` |
| `name` | `"${var.environment}-app"` |
| `tags` | `merge(var.tags, {` |
| `vpc_id` | `var.vpc_id` |

## References

- `aws_security_group.alb.id`
- `var.environment`
- `var.tags`
- `var.vpc_id`
