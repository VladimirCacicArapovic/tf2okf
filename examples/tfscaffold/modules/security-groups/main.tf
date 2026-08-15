variable "environment" {
  description = "Deployment environment used for naming the security groups."
  type        = string
}

variable "vpc_id" {
  description = "Identifier of the VPC where security groups are created."
  type        = string
}

variable "tags" {
  description = "Common tags applied to security group resources."
  type        = map(string)
}

resource "aws_security_group" "alb" {
  name        = "${var.environment}-alb"
  description = "Allow inbound HTTP traffic to the application load balancer"
  vpc_id      = var.vpc_id

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = merge(var.tags, {
    Name = "${var.environment}-alb-sg"
  })
}

resource "aws_security_group" "app" {
  name        = "${var.environment}-app"
  description = "Allow traffic from the ALB to ECS tasks"
  vpc_id      = var.vpc_id

  ingress {
    from_port       = 8080
    to_port         = 8080
    protocol        = "tcp"
    security_groups = [aws_security_group.alb.id]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = merge(var.tags, {
    Name = "${var.environment}-app-sg"
  })
}

output "alb_security_group_id" {
  value = aws_security_group.alb.id
}

output "app_security_group_id" {
  value = aws_security_group.app.id
}
