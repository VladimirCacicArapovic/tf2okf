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
  at: '2026-08-19T22:09:43Z'
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
  resource: ../../components/internal/main.tf
  author: process:terraform
- id: source-8
  resource: ../../components/network/main.tf
  author: process:terraform
- id: source-9
  resource: ../../components/notifications/main.tf
  author: process:terraform
- id: source-10
  resource: ../../components/observability/main.tf
  author: process:terraform
- id: source-11
  resource: ../../components/orders/main.tf
  author: process:terraform
- id: source-12
  resource: ../../components/payments/main.tf
  author: process:terraform
- id: source-13
  resource: ../../components/security/main.tf
  author: process:terraform
- id: source-14
  resource: ../../modules/ecs-service/main.tf
  author: process:terraform
- id: source-15
  resource: ../../modules/security-groups/main.tf
  author: process:terraform
- id: source-16
  resource: ../../modules/tags/main.tf
  author: process:terraform
- id: source-17
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
  n6["component/internal"]
  n7["component/network"]
  n8["component/notifications"]
  n9["component/observability"]
  n10["component/orders"]
  n11["component/payments"]
  n12["component/security"]
  n13["shared-module/ecs-service"]
  n14["shared-module/security-groups"]
  n15["shared-module/tags"]
  n16["shared-module/vpc"]
  n0 --> n15
  n0 --> n16
  n1 --> n13
  n1 --> n15
  n10 --> n13
  n10 --> n15
  n11 --> n13
  n11 --> n15
  n12 --> n14
  n12 --> n15
  n2 --> n13
  n2 --> n15
  n3 --> n13
  n3 --> n15
  n4 --> n15
  n4 --> n16
  n5 --> n14
  n5 --> n15
  n6 --> n14
  n6 --> n15
  n7 --> n15
  n7 --> n16
  n8 --> n13
  n8 --> n15
  n9 --> n13
  n9 --> n15
```

## Edges

- `n0` -> `n15`
- `n0` -> `n16`
- `n1` -> `n13`
- `n1` -> `n15`
- `n10` -> `n13`
- `n10` -> `n15`
- `n11` -> `n13`
- `n11` -> `n15`
- `n12` -> `n14`
- `n12` -> `n15`
- `n2` -> `n13`
- `n2` -> `n15`
- `n3` -> `n13`
- `n3` -> `n15`
- `n4` -> `n15`
- `n4` -> `n16`
- `n5` -> `n14`
- `n5` -> `n15`
- `n6` -> `n14`
- `n6` -> `n15`
- `n7` -> `n15`
- `n7` -> `n16`
- `n8` -> `n13`
- `n8` -> `n15`
- `n9` -> `n13`
- `n9` -> `n15`
