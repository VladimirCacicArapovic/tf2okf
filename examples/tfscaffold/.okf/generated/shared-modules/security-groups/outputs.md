---
type: Terraform Outputs
title: security-groups Outputs
description: Outputs for tfscaffold module `security-groups`.
tags:
- terraform
- tfscaffold
- module
- outputs
generated:
  by: tf2okf/0.4.0
  at: '2026-08-15T09:33:39Z'
sources:
- id: source-1
  resource: ../../../../modules/security-groups/main.tf
  author: process:terraform
---


# security-groups Outputs

These outputs summarize what this tfscaffold unit exposes to other components or operators.

| Name | Value | Sensitive | Description |
|---|---|---|---|
| `alb_security_group_id` | `aws_security_group.alb.id` | false |  |
| `app_security_group_id` | `aws_security_group.app.id` | false |  |
