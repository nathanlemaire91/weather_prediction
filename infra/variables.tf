variable "bucket_name" {
  description = "Name of the S3 bucket"
  type        = string
  default     = "weather-prediction-bucket-dev"
}

variable "region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

variable "environment" {
  description = "Environment tag for the bucket"
  type        = string
  default     = "dev"
}

variable "rds_db_password" {
  description = "RDS root user password"
  type        = string
  sensitive   = true
}

variable "image_tag" {
  description = "Lambda function image tag"
  type        = string
}
