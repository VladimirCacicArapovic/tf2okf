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
  description = "Deployment environment for internal security infrastructure."
  type        = string
}

variable "region" {
  description = "AWS region where internal security is deployed."
  type        = string
}

variable "component_name" {
  description = "Logical internal component name."
  type        = string
  default     = "internal"
}

variable "vpc_id" {
  description = "VPC id where internal security groups are created."
  type        = string
}

variable "extra_tags" {
  description = "Extra tags for internal security resources."
  type        = map(string)
  default     = {}
}

locals {
  internal_environment = "${var.environment}-${var.component_name}"
  internal_tags = merge(module.tags.tags, var.extra_tags, {
    Component = var.component_name
    Exposure  = "private"
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
  environment = local.internal_environment
  vpc_id      = var.vpc_id
  tags        = local.internal_tags
}

output "alb_security_group_id" {
  value = module.security_groups.alb_security_group_id
}

output "app_security_group_id" {
  value = module.security_groups.app_security_group_id
}

