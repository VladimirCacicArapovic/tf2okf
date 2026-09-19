---
type: Terraform Outputs
title: internal Outputs
description: Outputs for tfscaffold component `internal`.
tags:
- terraform
- tfscaffold
- component
- outputs
generated:
  by: tf2okf/0.4.0
  at: '2026-09-19T10:27:39Z'
sources:
- id: source-1
  resource: ../../../../components/internal/main.tf
  author: process:terraform
---


# internal Outputs

These outputs summarize what this tfscaffold unit exposes to other components or operators.

| Name | Value | Sensitive | Description |
|---|---|---|---|
| `alb_security_group_id` | `module.security_groups.alb_security_group_id` | false |  |
| `app_security_group_id` | `module.security_groups.app_security_group_id` | false |  |
