---
type: Terraform Inputs
title: edge Inputs
description: Inputs for tfscaffold component `edge`.
tags:
- terraform
- tfscaffold
- component
- inputs
generated:
  by: tf2okf/0.4.0
  at: '2026-09-17T19:58:26Z'
sources:
- id: source-1
  resource: ../../../../components/edge/main.tf
  author: process:terraform
---


# edge Inputs

These inputs describe the values expected by this tfscaffold unit, including defaults and captured descriptions.

| Name | Type | Default | Sensitive | Description |
|---|---|---|---|---|
| `component_name` | `string` | `"edge"` | false | Logical edge component name. |
| `environment` | `string` | `required` | false | Deployment environment for edge security infrastructure. |
| `extra_tags` | `map(string)` | `{}` | false | Extra tags for edge security resources. |
| `region` | `string` | `required` | false | AWS region where edge security is deployed. |
| `service_port` | `number` | `8080` | false | Application ingress port exposed by edge tier. |
| `vpc_id` | `string` | `required` | false | VPC id where edge security groups are created. |
