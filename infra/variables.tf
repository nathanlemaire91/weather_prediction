variable "bucket_name" {
  description = "Name of the S3 bucket"
  type        = string
  default     = "bucket_hello_world"
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
