provider "aws" {
  region = var.region
}

resource "aws_s3_bucket" "weather_bucket" {
  bucket = var.bucket_name
  acl    = "private"

  versioning {
    enabled = true
  }

  tags = {
    Name        = var.bucket_name
    Environment = var.environment
  }
}
