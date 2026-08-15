---
type: Terraform Inputs
title: vpc Inputs
description: Inputs for tfscaffold module `vpc`.
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
  resource: ../../../../modules/vpc/main.tf
  author: process:terraform
---


# vpc Inputs

These inputs describe the values expected by this tfscaffold unit, including defaults and captured descriptions.

| Name | Type | Default | Sensitive | Description |
|---|---|---|---|---|
| `availability_zones` | `list(string)` | `required` | false | Availability zones used for distributing subnets across the region. |
| `environment` | `string` | `required` | false | Deployment environment used for naming the shared network resources. |
| `private_subnet_cidrs` | `list(string)` | `required` | false | CIDR blocks allocated to private subnets. |
| `public_subnet_cidrs` | `list(string)` | `required` | false | CIDR blocks allocated to public subnets. |
| `tags` | `map(string)` | `required` | false | Common tags applied to all networking resources. |
| `vpc_cidr` | `string` | `required` | false | CIDR block assigned to the VPC. |
