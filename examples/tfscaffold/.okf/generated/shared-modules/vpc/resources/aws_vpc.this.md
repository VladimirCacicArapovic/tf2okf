---
type: Terraform Resource
title: aws_vpc.this
description: Resource `aws_vpc.this` in tfscaffold module `vpc`.
tags:
- terraform
- tfscaffold
- module
- vpc
- resource
- aws_vpc
generated:
  by: tf2okf/0.4.0
  at: '2026-08-15T09:33:39Z'
resource: terraform://tfscaffold/module/vpc/aws_vpc.this
sources:
- id: source-1
  resource: ../../../../../modules/vpc/main.tf
  author: process:terraform
---


# aws_vpc.this

- tfscaffold Module: `vpc`
- File: `modules/vpc/main.tf`
- Terraform address: `aws_vpc.this`

## Configuration

| Attribute | Expression |
|---|---|
| `cidr_block` | `var.vpc_cidr` |
| `enable_dns_hostnames` | `true` |
| `enable_dns_support` | `true` |
| `tags` | `merge(var.tags, {` |

## References

- `var.environment`
- `var.tags`
- `var.vpc_cidr`
