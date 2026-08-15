---
type: Terraform Outputs
title: network Outputs
description: Outputs for tfscaffold component `network`.
tags:
- terraform
- tfscaffold
- component
- outputs
generated:
  by: tf2okf/0.4.0
  at: '2026-08-15T09:33:39Z'
sources:
- id: source-1
  resource: ../../../../components/network/main.tf
  author: process:terraform
---


# network Outputs

These outputs summarize what this tfscaffold unit exposes to other components or operators.

| Name | Value | Sensitive | Description |
|---|---|---|---|
| `private_subnet_ids` | `module.vpc.private_subnet_ids` | false |  |
| `public_subnet_ids` | `module.vpc.public_subnet_ids` | false |  |
| `vpc_id` | `module.vpc.vpc_id` | false |  |
