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
  description = "Deployment environment for analytics network infrastructure."
  type        = string
}

variable "region" {
  description = "AWS region where analytics network is provisioned."
  type        = string
}

variable "component_name" {
  description = "Logical analytics component name."
  type        = string
  default     = "analytics"
}

variable "vpc_cidr" {
  description = "CIDR block for the analytics VPC."
  type        = string
}

variable "availability_zones" {
  description = "Availability zones for analytics subnets."
  type        = list(string)
}

variable "private_subnet_cidrs" {
  description = "Private subnet CIDRs for analytics workloads."
  type        = list(string)
}

variable "public_subnet_cidrs" {
  description = "Public subnet CIDRs for analytics ingress resources."
  type        = list(string)
}

variable "extra_tags" {
  description = "Extra tags for analytics network resources."
  type        = map(string)
  default     = {}
}

locals {
  analytics_environment = "${var.environment}-${var.component_name}"
  network_tags = merge(module.tags.tags, var.extra_tags, {
    Component = var.component_name
    Layer     = "insights"
  })
}

module "tags" {
  source      = "../../modules/tags"
  environment = var.environment
  region      = var.region
  service     = "${var.component_name}-network"
}

module "vpc" {
  source               = "../../modules/vpc"
  environment          = local.analytics_environment
  vpc_cidr             = var.vpc_cidr
  availability_zones   = var.availability_zones
  private_subnet_cidrs = var.private_subnet_cidrs
  public_subnet_cidrs  = var.public_subnet_cidrs
  tags                 = local.network_tags
}

output "vpc_id" {
  value = module.vpc.vpc_id
}

output "private_subnet_ids" {
  value = module.vpc.private_subnet_ids
}

output "public_subnet_ids" {
  value = module.vpc.public_subnet_ids
}

