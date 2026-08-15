---
type: Terraform Inputs
title: tags Inputs
description: Inputs for tfscaffold module `tags`.
tags:
- terraform
- tfscaffold
- module
- inputs
generated:
  by: tf2okf/0.4.0
  at: '2026-08-15T09:33:39Z'
sources:
- id: source-1
  resource: ../../../../modules/tags/main.tf
  author: process:terraform
---


# tags Inputs

These inputs describe the values expected by this tfscaffold unit, including defaults and captured descriptions.

| Name | Type | Default | Sensitive | Description |
|---|---|---|---|---|
| `environment` | `string` | `required` | false | Deployment environment name to include in shared tags. |
| `region` | `string` | `required` | false | AWS region to include in shared tags. |
| `service` | `string` | `required` | false | Service or module name to include in shared tags. |
