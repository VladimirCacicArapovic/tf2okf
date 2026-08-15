---
type: Terraform Module Call
title: module.vpc
description: Module call `vpc` from tfscaffold component `network`.
tags:
- terraform
- tfscaffold
- component
- network
- module-call
generated:
  by: tf2okf/0.4.0
  at: '2026-08-15T09:33:39Z'
resource: terraform://tfscaffold/component/network/module.vpc
sources:
- id: source-1
  resource: ../../../../../components/network/main.tf
  author: process:terraform
---


# module.vpc

- Source: `../../modules/vpc`
- Defined in: `components/network/main.tf`

## References

- `module.tags.tags`
- `var.availability_zones`
- `var.environment`
- `var.private_subnet_cidrs`
- `var.public_subnet_cidrs`
- `var.vpc_cidr`
