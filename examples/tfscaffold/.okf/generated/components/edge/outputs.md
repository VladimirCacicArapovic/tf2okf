---
type: Terraform Outputs
title: edge Outputs
description: Outputs for tfscaffold component `edge`.
tags:
- terraform
- tfscaffold
- component
- outputs
generated:
  by: tf2okf/0.4.0
  at: '2026-08-19T22:09:43Z'
sources:
- id: source-1
  resource: ../../../../components/edge/main.tf
  author: process:terraform
---


# edge Outputs

These outputs summarize what this tfscaffold unit exposes to other components or operators.

| Name | Value | Sensitive | Description |
|---|---|---|---|
| `alb_security_group_id` | `module.security_groups.alb_security_group_id` | false |  |
| `app_security_group_id` | `module.security_groups.app_security_group_id` | false |  |
