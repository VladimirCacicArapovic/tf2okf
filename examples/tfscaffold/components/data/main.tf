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
  description = "Deployment environment for data network infrastructure."
  type        = string
}

variable "region" {
  description = "AWS region where data network is provisioned."
  type        = string
}

variable "component_name" {
  description = "Logical data component name."
  type        = string
  default     = "data"
}

variable "vpc_cidr" {
  description = "CIDR block for the data VPC."
  type        = string
}

variable "availability_zones" {
  description = "Availability zones for data subnets."
  type        = list(string)
}

variable "private_subnet_cidrs" {
  description = "Private subnet CIDRs for data workloads."
  type        = list(string)
}

variable "public_subnet_cidrs" {
  description = "Public subnet CIDRs for data ingress resources."
  type        = list(string)
}

variable "extra_tags" {
  description = "Extra tags for data network resources."
  type        = map(string)
  default     = {}
}

locals {
  data_environment = "${var.environment}-${var.component_name}"
  network_tags = merge(module.tags.tags, var.extra_tags, {
    Component = var.component_name
    Layer     = "platform"
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
  environment          = local.data_environment
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

