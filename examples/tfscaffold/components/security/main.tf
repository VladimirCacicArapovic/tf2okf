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
  description = "Deployment environment name used in resource naming and tagging."
  type        = string
}

variable "region" {
  description = "AWS region where security resources are provisioned."
  type        = string
}

variable "vpc_id" {
  description = "Identifier of the VPC where security groups should be created."
  type        = string
}

module "tags" {
  source      = "../../modules/tags"
  environment = var.environment
  region      = var.region
  service     = "security"
}

module "security_groups" {
  source      = "../../modules/security-groups"
  environment = var.environment
  vpc_id      = var.vpc_id
  tags        = module.tags.tags
}

output "alb_security_group_id" {
  value = module.security_groups.alb_security_group_id
}

output "app_security_group_id" {
  value = module.security_groups.app_security_group_id
}
