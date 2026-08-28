---
type: tfscaffold Terraform Unit
title: observability
description: Terraform component `observability` managed in a tfscaffold repository.
tags:
- terraform
- tfscaffold
- component
- observability
generated:
  by: tf2okf/0.4.0
  at: '2026-08-19T22:09:43Z'
sources:
- id: source-1
  resource: ../../../../components/observability/main.tf
  author: process:terraform
---


# observability

This tfscaffold component summarizes the Terraform root under `components/observability` and highlights its interface, dependencies, and generated references.

Kind: **tfscaffold component**

Source directory: `components/observability`

- Resources/data sources: **0**
- Module calls: **2**
- Inputs: **11**
- Outputs: **2**

## Component description

<!-- tf2okf:manual-description-start -->
Add a detailed description of what this component is for, how it is used, and any operational caveats. Anything between the marker comments is preserved by `tf2okf generate`.
<!-- tf2okf:manual-description-end -->

## Knowledge

* [Inputs](inputs.md)
* [Outputs](outputs.md)
* [Providers](providers.md)
* [Dependencies](dependencies.md)

## Module calls

* [module.ecs_service](module-calls/ecs_service.md)
* [module.tags](module-calls/tags.md)
