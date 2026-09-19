---
type: tfscaffold Terraform Unit
title: security
description: Terraform component `security` managed in a tfscaffold repository.
tags:
- terraform
- tfscaffold
- component
- security
generated:
  by: tf2okf/0.4.0
  at: '2026-09-19T10:27:39Z'
sources:
- id: source-1
  resource: ../../../../components/security/main.tf
  author: process:terraform
---


# security

This tfscaffold component summarizes the Terraform root under `components/security` and highlights its interface, dependencies, and generated references.

Kind: **tfscaffold component**

Source directory: `components/security`

- Resources/data sources: **0**
- Module calls: **2**
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

## Module calls

* [module.security_groups](module-calls/security_groups.md)
* [module.tags](module-calls/tags.md)
