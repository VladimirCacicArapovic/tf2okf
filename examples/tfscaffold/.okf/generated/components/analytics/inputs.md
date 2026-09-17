---
type: Terraform Inputs
title: analytics Inputs
description: Inputs for tfscaffold component `analytics`.
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
  resource: ../../../../components/analytics/main.tf
  author: process:terraform
---


# analytics Inputs

These inputs describe the values expected by this tfscaffold unit, including defaults and captured descriptions.

| Name | Type | Default | Sensitive | Description |
|---|---|---|---|---|
| `availability_zones` | `list(string)` | `required` | false | Availability zones for analytics subnets. |
| `component_name` | `string` | `"analytics"` | false | Logical analytics component name. |
| `environment` | `string` | `required` | false | Deployment environment for analytics network infrastructure. |
| `extra_tags` | `map(string)` | `{}` | false | Extra tags for analytics network resources. |
| `private_subnet_cidrs` | `list(string)` | `required` | false | Private subnet CIDRs for analytics workloads. |
| `public_subnet_cidrs` | `list(string)` | `required` | false | Public subnet CIDRs for analytics ingress resources. |
| `region` | `string` | `required` | false | AWS region where analytics network is provisioned. |
| `vpc_cidr` | `string` | `required` | false | CIDR block for the analytics VPC. |
