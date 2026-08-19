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
  description = "Deployment environment for observability infrastructure."
  type        = string
}

variable "region" {
  description = "AWS region where observability is deployed."
  type        = string
}

variable "component_name" {
  description = "Logical observability component name."
  type        = string
  default     = "observability"
}

variable "container_image" {
  description = "Container image URI for observability collector."
  type        = string
}

variable "container_port" {
  description = "Container port for observability collector."
  type        = number
  default     = 4318
}

variable "vpc_id" {
  description = "VPC id for observability networking."
  type        = string
}

variable "private_subnet_ids" {
  description = "Private subnets for observability ECS tasks."
  type        = list(string)
}

variable "public_subnet_ids" {
  description = "Public subnets for observability ALB."
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
  description = "Extra tags for observability resources."
  type        = map(string)
  default     = {}
}

locals {
  effective_service_name = "${var.component_name}-${var.environment}"
  observability_tags = merge(module.tags.tags, var.extra_tags, {
    Component = var.component_name
    Purpose   = "telemetry"
  })
}

module "tags" {
  source      = "../../modules/tags"
  environment = var.environment
  region      = var.region
  service     = var.component_name
}

module "ecs_service" {
  source                = "../../modules/ecs-service"
  environment           = var.environment
  app_name              = local.effective_service_name
  container_image       = var.container_image
  container_port        = var.container_port
  vpc_id                = var.vpc_id
  private_subnet_ids    = var.private_subnet_ids
  public_subnet_ids     = var.public_subnet_ids
  alb_security_group_id = var.alb_security_group_id
  app_security_group_id = var.app_security_group_id
  tags                  = local.observability_tags
}

output "service_name" {
  value = module.ecs_service.service_name
}

output "alb_dns_name" {
  value = module.ecs_service.alb_dns_name
}

