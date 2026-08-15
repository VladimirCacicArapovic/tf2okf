---
type: Terraform Resource
title: aws_security_group.alb
description: Resource `aws_security_group.alb` in tfscaffold module `security-groups`.
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
resource: terraform://tfscaffold/module/security-groups/aws_security_group.alb
sources:
- id: source-1
  resource: ../../../../../modules/security-groups/main.tf
  author: process:terraform
---


# aws_security_group.alb

- tfscaffold Module: `security-groups`
- File: `modules/security-groups/main.tf`
- Terraform address: `aws_security_group.alb`

## Configuration

| Attribute | Expression |
|---|---|
| `description` | `"Allow inbound HTTP traffic to the application load balancer"` |
| `name` | `"${var.environment}-alb"` |
| `tags` | `merge(var.tags, {` |
| `vpc_id` | `var.vpc_id` |

## References

- `var.environment`
- `var.tags`
- `var.vpc_id`
