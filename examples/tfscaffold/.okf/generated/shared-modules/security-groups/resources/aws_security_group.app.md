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
  at: '2026-09-17T19:58:26Z'
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
| `cidr_blocks` | `["0.0.0.0/0"]` |
| `description` | `"Allow traffic from the ALB to ECS tasks"` |
| `from_port` | `0` |
| `name` | `"${var.environment}-app"` |
| `protocol` | `"-1"` |
| `security_groups` | `[aws_security_group.alb.id]` |
| `tags` | `merge(var.tags, {
Name = "${var.environment}-app-sg"
})` |
| `to_port` | `0` |
| `vpc_id` | `var.vpc_id` |

## References

- `aws_security_group.alb.id`
- `var.environment`
- `var.tags`
- `var.vpc_id`
