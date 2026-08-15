variable "environment" {
  description = "Deployment environment used for naming ECS and ALB resources."
  type        = string
}

variable "app_name" {
  description = "Logical application name used across ECS service resources."
  type        = string
}

variable "container_image" {
  description = "Container image URI deployed to the ECS task definition."
  type        = string
}

variable "container_port" {
  description = "Container port exposed by the application workload."
  type        = number
}

variable "vpc_id" {
  description = "Identifier of the VPC hosting the ECS service and load balancer."
  type        = string
}

variable "private_subnet_ids" {
  description = "Private subnet identifiers used for ECS task networking."
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
  description = "Security group identifier attached to ECS service tasks."
  type        = string
}

variable "tags" {
  description = "Common tags applied to ECS, load balancer, and target group resources."
  type        = map(string)
}

resource "aws_ecs_cluster" "this" {
  name = "${var.environment}-${var.app_name}"

  tags = merge(var.tags, {
    Name = "${var.environment}-${var.app_name}-cluster"
  })
}

resource "aws_lb" "this" {
  name               = substr("${var.environment}-${var.app_name}-alb", 0, 32)
  internal           = false
  load_balancer_type = "application"
  security_groups    = [var.alb_security_group_id]
  subnets            = var.public_subnet_ids

  tags = merge(var.tags, {
    Name = "${var.environment}-${var.app_name}-alb"
  })
}

resource "aws_lb_target_group" "this" {
  name        = substr("${var.environment}-${var.app_name}-tg", 0, 32)
  port        = var.container_port
  protocol    = "HTTP"
  target_type = "ip"
  vpc_id      = var.vpc_id

  health_check {
    path = "/health"
  }

  tags = merge(var.tags, {
    Name = "${var.environment}-${var.app_name}-tg"
  })
}

resource "aws_lb_listener" "http" {
  load_balancer_arn = aws_lb.this.arn
  port              = 80
  protocol          = "HTTP"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.this.arn
  }
}

resource "aws_ecs_task_definition" "this" {
  family                   = "${var.environment}-${var.app_name}"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = "256"
  memory                   = "512"

  container_definitions = jsonencode([
    {
      name  = var.app_name
      image = var.container_image
      portMappings = [
        {
          containerPort = var.container_port
          protocol      = "tcp"
        }
      ]
      essential = true
    }
  ])

  tags = merge(var.tags, {
    Name = "${var.environment}-${var.app_name}-task"
  })
}

resource "aws_ecs_service" "this" {
  name            = "${var.environment}-${var.app_name}"
  cluster         = aws_ecs_cluster.this.id
  task_definition = aws_ecs_task_definition.this.arn
  desired_count   = 2
  launch_type     = "FARGATE"

  network_configuration {
    assign_public_ip = false
    security_groups  = [var.app_security_group_id]
    subnets          = var.private_subnet_ids
  }

  load_balancer {
    container_name   = var.app_name
    container_port   = var.container_port
    target_group_arn = aws_lb_target_group.this.arn
  }

  depends_on = [aws_lb_listener.http]

  tags = merge(var.tags, {
    Name = "${var.environment}-${var.app_name}-service"
  })
}

output "service_name" {
  value = aws_ecs_service.this.name
}

output "alb_dns_name" {
  value = aws_lb.this.dns_name
}
