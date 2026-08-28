---
type: Terraform Inputs
title: data Inputs
description: Inputs for tfscaffold component `data`.
tags:
- terraform
- tfscaffold
- component
- inputs
generated:
  by: tf2okf/0.4.0
  at: '2026-08-19T22:09:43Z'
sources:
- id: source-1
  resource: ../../../../components/data/main.tf
  author: process:terraform
---


# data Inputs

These inputs describe the values expected by this tfscaffold unit, including defaults and captured descriptions.

| Name | Type | Default | Sensitive | Description |
|---|---|---|---|---|
| `availability_zones` | `list(string)` | `required` | false | Availability zones for data subnets. |
| `component_name` | `string` | `"data"` | false | Logical data component name. |
| `environment` | `string` | `required` | false | Deployment environment for data network infrastructure. |
| `extra_tags` | `map(string)` | `{}` | false | Extra tags for data network resources. |
| `private_subnet_cidrs` | `list(string)` | `required` | false | Private subnet CIDRs for data workloads. |
| `public_subnet_cidrs` | `list(string)` | `required` | false | Public subnet CIDRs for data ingress resources. |
| `region` | `string` | `required` | false | AWS region where data network is provisioned. |
| `vpc_cidr` | `string` | `required` | false | CIDR block for the data VPC. |
