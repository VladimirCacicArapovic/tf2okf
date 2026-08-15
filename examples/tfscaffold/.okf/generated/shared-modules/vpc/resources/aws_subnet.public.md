---
type: Terraform Resource
title: aws_subnet.public
description: Resource `aws_subnet.public` in tfscaffold module `vpc`.
tags:
- terraform
- tfscaffold
- module
- vpc
- resource
- aws_subnet
generated:
  by: tf2okf/0.4.0
  at: '2026-08-15T09:33:39Z'
resource: terraform://tfscaffold/module/vpc/aws_subnet.public
sources:
- id: source-1
  resource: ../../../../../modules/vpc/main.tf
  author: process:terraform
---


# aws_subnet.public

- tfscaffold Module: `vpc`
- File: `modules/vpc/main.tf`
- Terraform address: `aws_subnet.public`

## Configuration

| Attribute | Expression |
|---|---|
| `availability_zone` | `var.availability_zones[count.index]` |
| `cidr_block` | `var.public_subnet_cidrs[count.index]` |
| `count` | `length(var.public_subnet_cidrs)` |
| `map_public_ip_on_launch` | `true` |
| `tags` | `merge(var.tags, {` |
| `vpc_id` | `aws_vpc.this.id` |

## References

- `aws_vpc.this.id`
- `count.index`
- `var.availability_zones`
- `var.environment`
- `var.public_subnet_cidrs`
- `var.tags`
