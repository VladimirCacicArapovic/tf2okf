---
type: Terraform Dependency Graph
title: network Dependencies
description: Reference graph for tfscaffold component `network`.
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
  resource: ../../../../components/network/main.tf
  author: process:terraform
---


# network Dependencies

This graph shows which resources or module calls in the unit refer to other Terraform objects.

Edges are `consumer → referenced dependency`.

```mermaid
graph TD
  n0["module.tags"]
  n1["module.vpc"]
  n1 --> n0
```
