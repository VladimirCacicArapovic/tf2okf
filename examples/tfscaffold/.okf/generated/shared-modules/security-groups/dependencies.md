---
type: Terraform Dependency Graph
title: security-groups Dependencies
description: Reference graph for tfscaffold module `security-groups`.
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
  resource: ../../../../modules/security-groups/main.tf
  author: process:terraform
---


# security-groups Dependencies

This graph shows which resources or module calls in the unit refer to other Terraform objects.

Edges are `consumer → referenced dependency`.

```mermaid
graph TD
  n0["aws_security_group.alb"]
  n1["aws_security_group.app"]
  n1 --> n0
```
