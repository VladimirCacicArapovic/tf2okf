---
type: Terraform Outputs
title: data Outputs
description: Outputs for tfscaffold component `data`.
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
  resource: ../../../../components/data/main.tf
  author: process:terraform
---


# data Outputs

These outputs summarize what this tfscaffold unit exposes to other components or operators.

| Name | Value | Sensitive | Description |
|---|---|---|---|
| `private_subnet_ids` | `module.vpc.private_subnet_ids` | false |  |
| `public_subnet_ids` | `module.vpc.public_subnet_ids` | false |  |
| `vpc_id` | `module.vpc.vpc_id` | false |  |
