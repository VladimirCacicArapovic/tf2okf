---
type: Terraform Inputs
title: network Inputs
description: Inputs for tfscaffold component `network`.
tags:
- terraform
- tfscaffold
- component
- inputs
generated:
  by: tf2okf/0.4.0
  at: '2026-08-15T09:33:39Z'
sources:
- id: source-1
  resource: ../../../../components/network/main.tf
  author: process:terraform
---


# network Inputs

These inputs describe the values expected by this tfscaffold unit, including defaults and captured descriptions.

| Name | Type | Default | Sensitive | Description |
|---|---|---|---|---|
| `availability_zones` | `list(string)` | `required` | false | Availability zones used to spread public and private subnets. |
| `environment` | `string` | `required` | false | Deployment environment name used in resource naming and tagging. |
| `private_subnet_cidrs` | `list(string)` | `required` | false | CIDR blocks for private application subnets. |
| `public_subnet_cidrs` | `list(string)` | `required` | false | CIDR blocks for public ingress-facing subnets. |
| `region` | `string` | `required` | false | AWS region where shared networking resources are provisioned. |
| `vpc_cidr` | `string` | `required` | false | CIDR block assigned to the shared VPC. |
