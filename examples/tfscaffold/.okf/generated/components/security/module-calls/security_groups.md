---
type: Terraform Module Call
title: module.security_groups
description: Module call `security_groups` from tfscaffold component `security`.
tags:
- terraform
- tfscaffold
- component
- security
- module-call
generated:
  by: tf2okf/0.4.0
  at: '2026-08-15T09:33:39Z'
resource: terraform://tfscaffold/component/security/module.security_groups
sources:
- id: source-1
  resource: ../../../../../components/security/main.tf
  author: process:terraform
---


# module.security_groups

- Source: `../../modules/security-groups`
- Defined in: `components/security/main.tf`

## References

- `module.tags.tags`
- `var.environment`
- `var.vpc_id`
