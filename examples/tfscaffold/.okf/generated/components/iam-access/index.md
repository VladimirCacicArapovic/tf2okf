---
type: tfscaffold Terraform Unit
title: iam-access
description: Terraform component `iam-access` managed in a tfscaffold repository.
tags:
- terraform
- tfscaffold
- component
- iam-access
generated:
  by: tf2okf/0.4.0
  at: '2026-09-17T19:58:26Z'
sources:
- id: source-1
  resource: ../../../../components/iam-access/main.tf
  author: process:terraform
---


# iam-access

This tfscaffold component summarizes the Terraform root under `components/iam-access` and highlights its interface, dependencies, and generated references.

Kind: **tfscaffold component**

Source directory: `components/iam-access`

- Resources/data sources: **3**
- Module calls: **0**
- Inputs: **5**
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
* [IAM access](iam-access.md)

## Resources and data sources

* [aws_iam_group_policy_attachment.analyst_results_attach](resources/aws_iam_group_policy_attachment.analyst_results_attach.md)
* [aws_iam_policy.athena_results_access](resources/aws_iam_policy.athena_results_access.md)
* [data.aws_iam_policy_document.analyst_query_access](resources/data.aws_iam_policy_document.analyst_query_access.md)
