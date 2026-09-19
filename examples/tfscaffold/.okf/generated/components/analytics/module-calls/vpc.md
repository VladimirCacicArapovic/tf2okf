---
type: Terraform Module Call
title: module.vpc
description: Module call `vpc` from tfscaffold component `analytics`.
tags:
- terraform
- tfscaffold
- component
- analytics
- module-call
generated:
  by: tf2okf/0.4.0
  at: '2026-09-19T10:27:39Z'
resource: terraform://tfscaffold/component/analytics/module.vpc
sources:
- id: source-1
  resource: ../../../../../components/analytics/main.tf
  author: process:terraform
---


# module.vpc

- Source: `../../modules/vpc`
- Defined in: `components/analytics/main.tf`

## References

- `local.analytics_environment`
- `local.network_tags`
- `var.availability_zones`
- `var.private_subnet_cidrs`
- `var.public_subnet_cidrs`
- `var.vpc_cidr`
