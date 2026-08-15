variable "environment" {
  description = "Deployment environment name to include in shared tags."
  type        = string
}

variable "region" {
  description = "AWS region to include in shared tags."
  type        = string
}

variable "service" {
  description = "Service or module name to include in shared tags."
  type        = string
}

output "tags" {
  value = {
    Environment = var.environment
    Region      = var.region
    Service     = var.service
    ManagedBy   = "tfscaffold"
    Example     = "true"
  }
}
