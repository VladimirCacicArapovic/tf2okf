---
type: Terraform Dependency Graph
title: vpc Dependencies
description: Reference graph for tfscaffold module `vpc`.
tags:
- terraform
- tfscaffold
- module
- dependencies
generated:
  by: tf2okf/0.4.0
  at: '2026-08-15T09:33:39Z'
sources:
- id: source-1
  resource: ../../../../modules/vpc/main.tf
  author: process:terraform
---


# vpc Dependencies

This graph shows which resources or module calls in the unit refer to other Terraform objects.

Edges are `consumer → referenced dependency`.

```mermaid
graph TD
  n0["aws_internet_gateway.this"]
  n1["aws_subnet.private"]
  n2["aws_subnet.public"]
  n3["aws_vpc.this"]
  n0 --> n3
  n1 --> n3
  n2 --> n3
```
