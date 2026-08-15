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
  description = "AWS region where shared networking resources are provisioned."
  type        = string
}

variable "vpc_cidr" {
  description = "CIDR block assigned to the shared VPC."
  type        = string
}

variable "availability_zones" {
  description = "Availability zones used to spread public and private subnets."
  type        = list(string)
}

variable "private_subnet_cidrs" {
  description = "CIDR blocks for private application subnets."
  type        = list(string)
}

variable "public_subnet_cidrs" {
  description = "CIDR blocks for public ingress-facing subnets."
  type        = list(string)
}

module "tags" {
  source      = "../../modules/tags"
  environment = var.environment
  region      = var.region
  service     = "network"
}

module "vpc" {
  source               = "../../modules/vpc"
  environment          = var.environment
  vpc_cidr             = var.vpc_cidr
  availability_zones   = var.availability_zones
  private_subnet_cidrs = var.private_subnet_cidrs
  public_subnet_cidrs  = var.public_subnet_cidrs
  tags                 = module.tags.tags
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

# python3 docs/copilot_okf_benchmark.py add \
#   --scenario architecture \
#   --prompt-name app-dependencies \
#   --prompt-text "Explain how the application component depends on the network and security layers." \
#   --used-okf \
#   --okf-context ".okf/generated/index.md,.okf/generated/components/app/index.md,.okf/knowledge/architecture.md" \
#   --response-quality 5 \
#   --response-time-seconds 10 \
#   --answer-summary "Clear answer with correct dependency flow and less exploration." \
#   --notes "Asked Copilot to read OKF first"
