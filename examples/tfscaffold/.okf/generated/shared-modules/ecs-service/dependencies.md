---
type: Terraform Dependency Graph
title: ecs-service Dependencies
description: Reference graph for tfscaffold module `ecs-service`.
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
  resource: ../../../../modules/ecs-service/main.tf
  author: process:terraform
---


# ecs-service Dependencies

This graph shows which resources or module calls in the unit refer to other Terraform objects.

Edges are `consumer → referenced dependency`.

```mermaid
graph TD
  n0["aws_ecs_cluster.this"]
  n1["aws_ecs_service.this"]
  n2["aws_ecs_task_definition.this"]
  n3["aws_lb.this"]
  n4["aws_lb_listener.http"]
  n5["aws_lb_target_group.this"]
  n1 --> n0
  n1 --> n2
  n1 --> n4
  n1 --> n5
  n4 --> n3
  n4 --> n5
```
