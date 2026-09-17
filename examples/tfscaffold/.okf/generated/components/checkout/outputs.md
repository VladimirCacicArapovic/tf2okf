---
type: Terraform Outputs
title: checkout Outputs
description: Outputs for tfscaffold component `checkout`.
tags:
- terraform
- tfscaffold
- component
- outputs
generated:
  by: tf2okf/0.4.0
  at: '2026-09-17T19:58:26Z'
sources:
- id: source-1
  resource: ../../../../components/checkout/main.tf
  author: process:terraform
---


# checkout Outputs

These outputs summarize what this tfscaffold unit exposes to other components or operators.

| Name | Value | Sensitive | Description |
|---|---|---|---|
| `alb_dns_name` | `module.ecs_service.alb_dns_name` | false |  |
| `effective_service_name` | `local.effective_service_name` | false |  |
| `service_name` | `module.ecs_service.service_name` | false |  |
