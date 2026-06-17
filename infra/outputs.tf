output "bucket_id" {
  description = "The name (ID) of the S3 bucket"
  value       = aws_s3_bucket.weather_bucket.id
}

output "rds_hostname" {
  description = "RDS instance hostname"
  value       = aws_db_instance.weather-rds.address
  sensitive   = true
}

output "rds_port" {
  description = "RDS instance port"
  value       = aws_db_instance.weather-rds.port
  sensitive   = true
}

output "rds_username" {
  description = "RDS instance root username"
  value       = aws_db_instance.weather-rds.username
  sensitive   = true
}