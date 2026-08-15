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
  description = "AWS region where the application stack is provisioned."
  type        = string
}

variable "app_name" {
  description = "Logical application name used for ECS, ALB, and related resources."
  type        = string
}

variable "container_image" {
  description = "Container image URI deployed into the ECS service."
  type        = string
}

variable "container_port" {
  description = "Application port exposed by the running container."
  type        = number
}

variable "vpc_id" {
  description = "Identifier of the VPC hosting the load balancer and ECS service."
  type        = string
}

variable "private_subnet_ids" {
  description = "Private subnet identifiers used by the ECS service tasks."
  type        = list(string)
}

variable "public_subnet_ids" {
  description = "Public subnet identifiers used by the internet-facing ALB."
  type        = list(string)
}

variable "alb_security_group_id" {
  description = "Security group identifier attached to the application load balancer."
  type        = string
}

variable "app_security_group_id" {
  description = "Security group identifier attached to ECS tasks."
  type        = string
}

module "tags" {
  source      = "../../modules/tags"
  environment = var.environment
  region      = var.region
  service     = var.app_name
}

module "ecs_service" {
  source                = "../../modules/ecs-service"
  environment           = var.environment
  app_name              = var.app_name
  container_image       = var.container_image
  container_port        = var.container_port
  vpc_id                = var.vpc_id
  private_subnet_ids    = var.private_subnet_ids
  public_subnet_ids     = var.public_subnet_ids
  alb_security_group_id = var.alb_security_group_id
  app_security_group_id = var.app_security_group_id
  tags                  = module.tags.tags
}

output "service_name" {
  value = module.ecs_service.service_name
}

output "alb_dns_name" {
  value = module.ecs_service.alb_dns_name
}
