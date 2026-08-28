---
type: tfscaffold Terraform Unit
title: vpc
description: Terraform module `vpc` managed in a tfscaffold repository.
tags:
- terraform
- tfscaffold
- module
- vpc
generated:
  by: tf2okf/0.4.0
  at: '2026-08-19T22:09:43Z'
sources:
- id: source-1
  resource: ../../../../modules/vpc/main.tf
  author: process:terraform
---


# vpc

This tfscaffold module summarizes the Terraform root under `modules/vpc` and highlights its interface, dependencies, and generated references.

Kind: **tfscaffold module**

Source directory: `modules/vpc`

- Resources/data sources: **4**
- Module calls: **0**
- Inputs: **6**
- Outputs: **3**

## Component description

<!-- tf2okf:manual-description-start -->
Add a detailed description of what this component is for, how it is used, and any operational caveats. Anything between the marker comments is preserved by `tf2okf generate`.
<!-- tf2okf:manual-description-end -->

## Knowledge

* [Inputs](inputs.md)
* [Outputs](outputs.md)
* [Providers](providers.md)
* [Dependencies](dependencies.md)

## Resources and data sources

* [aws_internet_gateway.this](resources/aws_internet_gateway.this.md)
* [aws_subnet.private](resources/aws_subnet.private.md)
* [aws_subnet.public](resources/aws_subnet.public.md)
* [aws_vpc.this](resources/aws_vpc.this.md)
