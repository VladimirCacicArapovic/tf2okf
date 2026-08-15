---
type: Terraform Resource
title: aws_internet_gateway.this
description: Resource `aws_internet_gateway.this` in tfscaffold module `vpc`.
tags:
- terraform
- tfscaffold
- module
- vpc
- resource
- aws_internet_gateway
generated:
  by: tf2okf/0.4.0
  at: '2026-08-15T09:33:39Z'
resource: terraform://tfscaffold/module/vpc/aws_internet_gateway.this
sources:
- id: source-1
  resource: ../../../../../modules/vpc/main.tf
  author: process:terraform
---


# aws_internet_gateway.this

- tfscaffold Module: `vpc`
- File: `modules/vpc/main.tf`
- Terraform address: `aws_internet_gateway.this`

## Configuration

| Attribute | Expression |
|---|---|
| `tags` | `merge(var.tags, {` |
| `vpc_id` | `aws_vpc.this.id` |

## References

- `aws_vpc.this.id`
- `var.environment`
- `var.tags`
