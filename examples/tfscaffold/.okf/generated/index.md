# Generated tfscaffold Knowledge

Components: **14**  
Shared modules: **4**

* [Environments](environments.md) - Environment/version tfvars discovered under `etc/`.
* [Topology](topology.md) - Component to shared-module composition graph.

## Components

* [analytics](components/analytics/) - independent Terraform root module.
* [app](components/app/) - independent Terraform root module.
* [catalog](components/catalog/) - independent Terraform root module.
* [checkout](components/checkout/) - independent Terraform root module.
* [data](components/data/) - independent Terraform root module.
* [edge](components/edge/) - independent Terraform root module.
* [iam-access](components/iam-access/) - independent Terraform root module.
* [internal](components/internal/) - independent Terraform root module.
* [network](components/network/) - independent Terraform root module.
* [notifications](components/notifications/) - independent Terraform root module.
* [observability](components/observability/) - independent Terraform root module.
* [orders](components/orders/) - independent Terraform root module.
* [payments](components/payments/) - independent Terraform root module.
* [security](components/security/) - independent Terraform root module.

## Shared modules

* [ecs-service](shared-modules/ecs-service/) - reusable Terraform module.
* [security-groups](shared-modules/security-groups/) - reusable Terraform module.
* [tags](shared-modules/tags/) - reusable Terraform module.
* [vpc](shared-modules/vpc/) - reusable Terraform module.
