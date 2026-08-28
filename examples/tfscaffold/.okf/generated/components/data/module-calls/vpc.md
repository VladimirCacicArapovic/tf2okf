---
type: Terraform Module Call
title: module.vpc
description: Module call `vpc` from tfscaffold component `data`.
tags:
- terraform
- tfscaffold
- component
- data
- module-call
generated:
  by: tf2okf/0.4.0
  at: '2026-08-19T22:09:43Z'
resource: terraform://tfscaffold/component/data/module.vpc
sources:
- id: source-1
  resource: ../../../../../components/data/main.tf
  author: process:terraform
---


# module.vpc

- Source: `../../modules/vpc`
- Defined in: `components/data/main.tf`

## References

- `local.data_environment`
- `local.network_tags`
- `var.availability_zones`
- `var.private_subnet_cidrs`
- `var.public_subnet_cidrs`
- `var.vpc_cidr`
