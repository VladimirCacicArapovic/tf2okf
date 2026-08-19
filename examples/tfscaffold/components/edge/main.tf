terraform {
  required_version = ">= 1.6.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

variable "environment" {
  description = "Deployment environment for edge security infrastructure."
  type        = string
}

variable "region" {
  description = "AWS region where edge security is deployed."
  type        = string
}

variable "component_name" {
  description = "Logical edge component name."
  type        = string
  default     = "edge"
}

variable "vpc_id" {
  description = "VPC id where edge security groups are created."
  type        = string
}

variable "service_port" {
  description = "Application ingress port exposed by edge tier."
  type        = number
  default     = 8080
}

variable "extra_tags" {
  description = "Extra tags for edge security resources."
  type        = map(string)
  default     = {}
}

locals {
  edge_environment = "${var.environment}-${var.component_name}"
  edge_tags = merge(module.tags.tags, var.extra_tags, {
    Component = var.component_name
    Port      = tostring(var.service_port)
  })
}

module "tags" {
  source      = "../../modules/tags"
  environment = var.environment
  region      = var.region
  service     = "${var.component_name}-security"
}

module "security_groups" {
  source      = "../../modules/security-groups"
  environment = local.edge_environment
  vpc_id      = var.vpc_id
  tags        = local.edge_tags
}

output "alb_security_group_id" {
  value = module.security_groups.alb_security_group_id
}

output "app_security_group_id" {
  value = module.security_groups.app_security_group_id
}

