---
type: Terraform Outputs
title: ecs-service Outputs
description: Outputs for tfscaffold module `ecs-service`.
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
  resource: ../../../../modules/ecs-service/main.tf
  author: process:terraform
---


# ecs-service Outputs

These outputs summarize what this tfscaffold unit exposes to other components or operators.

| Name | Value | Sensitive | Description |
|---|---|---|---|
| `alb_dns_name` | `aws_lb.this.dns_name` | false |  |
| `service_name` | `aws_ecs_service.this.name` | false |  |
