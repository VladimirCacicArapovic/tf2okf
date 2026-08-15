---
type: Terraform Outputs
title: vpc Outputs
description: Outputs for tfscaffold module `vpc`.
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
  resource: ../../../../modules/vpc/main.tf
  author: process:terraform
---


# vpc Outputs

These outputs summarize what this tfscaffold unit exposes to other components or operators.

| Name | Value | Sensitive | Description |
|---|---|---|---|
| `private_subnet_ids` | `aws_subnet.private[*].id` | false |  |
| `public_subnet_ids` | `aws_subnet.public[*].id` | false |  |
| `vpc_id` | `aws_vpc.this.id` | false |  |
