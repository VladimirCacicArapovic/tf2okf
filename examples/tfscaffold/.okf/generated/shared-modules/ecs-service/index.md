---
type: tfscaffold Terraform Unit
title: ecs-service
description: Terraform module `ecs-service` managed in a tfscaffold repository.
tags:
- terraform
- tfscaffold
- module
- ecs-service
generated:
  by: tf2okf/0.4.0
  at: '2026-08-15T09:33:39Z'
sources:
- id: source-1
  resource: ../../../../modules/ecs-service/main.tf
  author: process:terraform
---


# ecs-service

This tfscaffold module summarizes the Terraform root under `modules/ecs-service` and highlights its interface, dependencies, and generated references.

Kind: **tfscaffold module**

Source directory: `modules/ecs-service`

- Resources/data sources: **6**
- Module calls: **0**
- Inputs: **10**
- Outputs: **2**

## Knowledge

* [Inputs](inputs.md)
* [Outputs](outputs.md)
* [Providers](providers.md)
* [Dependencies](dependencies.md)

## Resources and data sources

* [aws_ecs_cluster.this](resources/aws_ecs_cluster.this.md)
* [aws_ecs_service.this](resources/aws_ecs_service.this.md)
* [aws_ecs_task_definition.this](resources/aws_ecs_task_definition.this.md)
* [aws_lb.this](resources/aws_lb.this.md)
* [aws_lb_listener.http](resources/aws_lb_listener.http.md)
* [aws_lb_target_group.this](resources/aws_lb_target_group.this.md)
