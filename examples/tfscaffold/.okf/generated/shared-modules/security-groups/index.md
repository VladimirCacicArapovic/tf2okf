---
type: tfscaffold Terraform Unit
title: security-groups
description: Terraform module `security-groups` managed in a tfscaffold repository.
tags:
- terraform
- tfscaffold
- module
- security-groups
generated:
  by: tf2okf/0.4.0
  at: '2026-09-17T19:58:26Z'
sources:
- id: source-1
  resource: ../../../../modules/security-groups/main.tf
  author: process:terraform
---


# security-groups

This tfscaffold module summarizes the Terraform root under `modules/security-groups` and highlights its interface, dependencies, and generated references.

Kind: **tfscaffold module**

Source directory: `modules/security-groups`

- Resources/data sources: **2**
- Module calls: **0**
- Inputs: **3**
- Outputs: **2**

## Component description

<!-- tf2okf:manual-description-start -->
Add a detailed description of what this component is for, who consumes it, where permissions or access are attached, and any operational caveats. Anything between the marker comments is preserved by `tf2okf generate`.
<!-- tf2okf:manual-description-end -->

## Knowledge

* [Inputs](inputs.md)
* [Outputs](outputs.md)
* [Providers](providers.md)
* [Dependencies](dependencies.md)

## Resources and data sources

* [aws_security_group.alb](resources/aws_security_group.alb.md)
* [aws_security_group.app](resources/aws_security_group.app.md)
