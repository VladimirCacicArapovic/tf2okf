---
type: Terraform Outputs
title: observability Outputs
description: Outputs for tfscaffold component `observability`.
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
  resource: ../../../../components/observability/main.tf
  author: process:terraform
---


# observability Outputs

These outputs summarize what this tfscaffold unit exposes to other components or operators.

| Name | Value | Sensitive | Description |
|---|---|---|---|
| `alb_dns_name` | `module.ecs_service.alb_dns_name` | false |  |
| `service_name` | `module.ecs_service.service_name` | false |  |
