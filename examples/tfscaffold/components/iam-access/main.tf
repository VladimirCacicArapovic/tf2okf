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
  description = "Deployment environment for IAM access examples."
  type        = string
}

variable "region" {
  description = "AWS region where IAM access examples are evaluated."
  type        = string
}

variable "analytics_bucket_arn" {
  description = "S3 bucket ARN used by analytics principals for Athena query results."
  type        = string
  default     = "arn:aws:s3:::example-analytics-results"
}

variable "glue_catalog_arn" {
  description = "Glue catalog ARN used by analytics principals."
  type        = string
  default     = "arn:aws:glue:eu-west-2:123456789012:catalog"
}

variable "data_analyst_group_name" {
  description = "IAM group representing analyst users."
  type        = string
  default     = "data-analyst-team"
}

locals {
  athena_workgroup_arn = "arn:aws:athena:${var.region}:123456789012:workgroup/analyst"
  glue_database_arn    = "arn:aws:glue:${var.region}:123456789012:database/example_analytics"
}

data "aws_iam_policy_document" "analyst_query_access" {
  statement {
    sid    = "AthenaQuery"
    effect = "Allow"
    actions = [
      "athena:GetQueryExecution",
      "athena:GetQueryResults",
      "athena:ListWorkGroups",
      "athena:StartQueryExecution"
    ]
    resources = [
      local.athena_workgroup_arn,
      "*"
    ]
  }

  statement {
    sid    = "GlueRead"
    effect = "Allow"
    actions = [
      "glue:GetDatabase",
      "glue:GetDatabases",
      "glue:GetTable",
      "glue:GetTables"
    ]
    resources = [
      var.glue_catalog_arn,
      local.glue_database_arn
    ]
  }
}

resource "aws_iam_policy" "athena_results_access" {
  name = "${var.environment}-athena-results-access"
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid      = "AthenaResultsBucket"
        Effect   = "Allow"
        Action   = ["s3:GetObject", "s3:PutObject"]
        Resource = ["${var.analytics_bucket_arn}/*"]
      }
    ]
  })
}

resource "aws_iam_group_policy_attachment" "analyst_results_attach" {
  group      = var.data_analyst_group_name
  policy_arn = aws_iam_policy.athena_results_access.arn
}

output "analyst_policy_document_json" {
  description = "Rendered IAM policy document for analyst Athena and Glue access."
  value       = data.aws_iam_policy_document.analyst_query_access.json
}

output "results_policy_arn" {
  description = "Managed IAM policy ARN attached to the analyst group."
  value       = aws_iam_policy.athena_results_access.arn
}
