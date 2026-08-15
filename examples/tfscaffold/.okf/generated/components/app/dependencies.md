---
type: Terraform Dependency Graph
title: app Dependencies
description: Reference graph for tfscaffold component `app`.
tags:
- terraform
- tfscaffold
- component
- dependencies
generated:
  by: tf2okf/0.4.0
  at: '2026-08-15T09:33:39Z'
sources:
- id: source-1
  resource: ../../../../components/app/main.tf
  author: process:terraform
---


# app Dependencies

This graph shows which resources or module calls in the unit refer to other Terraform objects.

Edges are `consumer → referenced dependency`.

```mermaid
graph TD
  n0["module.ecs_service"]
  n1["module.tags"]
  n0 --> n1
```
