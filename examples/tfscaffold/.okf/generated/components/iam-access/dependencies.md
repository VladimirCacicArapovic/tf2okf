---
type: Terraform Dependency Graph
title: iam-access Dependencies
description: Reference graph for tfscaffold component `iam-access`.
tags:
- terraform
- tfscaffold
- component
- dependencies
generated:
  by: tf2okf/0.4.0
  at: '2026-09-19T10:27:39Z'
sources:
- id: source-1
  resource: ../../../../components/iam-access/main.tf
  author: process:terraform
---


# iam-access Dependencies

This graph shows which resources or module calls in the unit refer to other Terraform objects.

Edges are `consumer → referenced dependency`.

```mermaid
graph TD
  n0["aws_iam_group_policy_attachment.analyst_results_attach"]
  n1["aws_iam_policy.athena_results_access"]
  n2["data.aws_iam_policy_document.analyst_query_access"]
  n0 --> n1
```
