---
type: tfscaffold Topology
title: tfscaffold Topology
description: Cross-component and shared-module composition map.
tags:
- terraform
- tfscaffold
- topology
generated:
  by: tf2okf/0.4.0
  at: '2026-09-19T10:27:39Z'
sources:
- id: source-1
  resource: ../../components/analytics/main.tf
  author: process:terraform
- id: source-2
  resource: ../../components/app/main.tf
  author: process:terraform
- id: source-3
  resource: ../../components/catalog/main.tf
  author: process:terraform
- id: source-4
  resource: ../../components/checkout/main.tf
  author: process:terraform
- id: source-5
  resource: ../../components/data/main.tf
  author: process:terraform
- id: source-6
  resource: ../../components/edge/main.tf
  author: process:terraform
- id: source-7
  resource: ../../components/iam-access/main.tf
  author: process:terraform
- id: source-8
  resource: ../../components/internal/main.tf
  author: process:terraform
- id: source-9
  resource: ../../components/network/main.tf
  author: process:terraform
- id: source-10
  resource: ../../components/notifications/main.tf
  author: process:terraform
- id: source-11
  resource: ../../components/observability/main.tf
  author: process:terraform
- id: source-12
  resource: ../../components/orders/main.tf
  author: process:terraform
- id: source-13
  resource: ../../components/payments/main.tf
  author: process:terraform
- id: source-14
  resource: ../../components/security/main.tf
  author: process:terraform
- id: source-15
  resource: ../../modules/ecs-service/main.tf
  author: process:terraform
- id: source-16
  resource: ../../modules/security-groups/main.tf
  author: process:terraform
- id: source-17
  resource: ../../modules/tags/main.tf
  author: process:terraform
- id: source-18
  resource: ../../modules/vpc/main.tf
  author: process:terraform
---


# tfscaffold Topology

```mermaid
graph LR
  n0["component/analytics"]
  n1["component/app"]
  n2["component/catalog"]
  n3["component/checkout"]
  n4["component/data"]
  n5["component/edge"]
  n6["component/iam-access"]
  n7["component/internal"]
  n8["component/network"]
  n9["component/notifications"]
  n10["component/observability"]
  n11["component/orders"]
  n12["component/payments"]
  n13["component/security"]
  n14["shared-module/ecs-service"]
  n15["shared-module/security-groups"]
  n16["shared-module/tags"]
  n17["shared-module/vpc"]
  n0 --> n16
  n0 --> n17
  n1 --> n14
  n1 --> n16
  n10 --> n14
  n10 --> n16
  n11 --> n14
  n11 --> n16
  n12 --> n14
  n12 --> n16
  n13 --> n15
  n13 --> n16
  n2 --> n14
  n2 --> n16
  n3 --> n14
  n3 --> n16
  n4 --> n16
  n4 --> n17
  n5 --> n15
  n5 --> n16
  n7 --> n15
  n7 --> n16
  n8 --> n16
  n8 --> n17
  n9 --> n14
  n9 --> n16
```

## Edges

- `n0` -> `n16`
- `n0` -> `n17`
- `n1` -> `n14`
- `n1` -> `n16`
- `n10` -> `n14`
- `n10` -> `n16`
- `n11` -> `n14`
- `n11` -> `n16`
- `n12` -> `n14`
- `n12` -> `n16`
- `n13` -> `n15`
- `n13` -> `n16`
- `n2` -> `n14`
- `n2` -> `n16`
- `n3` -> `n14`
- `n3` -> `n16`
- `n4` -> `n16`
- `n4` -> `n17`
- `n5` -> `n15`
- `n5` -> `n16`
- `n7` -> `n15`
- `n7` -> `n16`
- `n8` -> `n16`
- `n8` -> `n17`
- `n9` -> `n14`
- `n9` -> `n16`
