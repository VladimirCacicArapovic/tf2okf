---
type: Terraform Outputs
title: catalog Outputs
description: Outputs for tfscaffold component `catalog`.
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
  resource: ../../../../components/catalog/main.tf
  author: process:terraform
---


# catalog Outputs

These outputs summarize what this tfscaffold unit exposes to other components or operators.

| Name | Value | Sensitive | Description |
|---|---|---|---|
| `alb_dns_name` | `module.ecs_service.alb_dns_name` | false |  |
| `service_name` | `module.ecs_service.service_name` | false |  |
