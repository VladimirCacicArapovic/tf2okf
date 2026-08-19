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
  description = "Deployment environment for checkout infrastructure."
  type        = string
}

variable "region" {
  description = "AWS region where checkout is deployed."
  type        = string
}

variable "component_name" {
  description = "Logical checkout component name."
  type        = string
  default     = "checkout"

  validation {
    condition     = length(var.component_name) >= 3
    error_message = "component_name must be at least 3 characters."
  }
}

variable "service_name_override" {
  description = "Optional explicit ECS service name."
  type        = string
  default     = ""
}

variable "container_image" {
  description = "Container image URI for checkout."
  type        = string
}

variable "container_port" {
  description = "Container port for checkout."
  type        = number
  default     = 8080
}

variable "desired_count" {
  description = "Desired ECS task count for checkout."
  type        = number
  default     = 2

  validation {
    condition     = var.desired_count >= 1 && var.desired_count <= 10
    error_message = "desired_count must be between 1 and 10."
  }
}

variable "vpc_id" {
  description = "VPC id for checkout networking."
  type        = string
}

variable "private_subnet_ids" {
  description = "Private subnets for checkout ECS tasks."
  type        = list(string)
}

variable "public_subnet_ids" {
  description = "Public subnets for checkout ALB."
  type        = list(string)
}

variable "alb_security_group_id" {
  description = "ALB security group id."
  type        = string
}

variable "app_security_group_id" {
  description = "Application security group id."
  type        = string
}

variable "extra_tags" {
  description = "Extra tags for checkout resources."
  type        = map(string)
  default     = {}
}

locals {
  effective_service_name = var.service_name_override != "" ? var.service_name_override : "${var.component_name}-${var.environment}"
  effective_port         = var.container_port > 0 ? var.container_port : 8080
}

module "tags" {
  source      = "../../modules/tags"
  environment = var.environment
  region      = var.region
  service     = var.component_name
}

locals {
  checkout_tags = merge(module.tags.tags, var.extra_tags, {
    Component = var.component_name
    Stack     = local.effective_service_name
  })
}

module "ecs_service" {
  source                = "../../modules/ecs-service"
  environment           = var.environment
  app_name              = local.effective_service_name
  container_image       = var.container_image
  container_port        = local.effective_port
  vpc_id                = var.vpc_id
  private_subnet_ids    = var.private_subnet_ids
  public_subnet_ids     = var.public_subnet_ids
  alb_security_group_id = var.alb_security_group_id
  app_security_group_id = var.app_security_group_id
  tags                  = local.checkout_tags
}

output "service_name" {
  value = module.ecs_service.service_name
}

output "alb_dns_name" {
  value = module.ecs_service.alb_dns_name
}

output "effective_service_name" {
  value = local.effective_service_name
}
