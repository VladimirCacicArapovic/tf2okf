terraform { required_providers { null = { source = "hashicorp/null" version = "~> 3.2" } } }
variable "environment" { type = string }
resource "null_resource" "example" { triggers = { env = var.environment } }
output "id" { value = null_resource.example.id }
