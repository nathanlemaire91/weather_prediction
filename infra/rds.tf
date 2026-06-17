resource "aws_db_instance" "weather-rds" {
  identifier             = "weather-rds"
  instance_class         = "db.t3.micro"
  allocated_storage      = 5
  engine                 = "postgres"
  engine_version         = "18.3"
  username               = "edu"
  password               = var.rds_db_password
  db_subnet_group_name   = aws_db_subnet_group.weather-subnet.name
  vpc_security_group_ids = [aws_security_group.weather-security-group.id]
  parameter_group_name   = aws_db_parameter_group.weather-pgroup.name
  publicly_accessible    = true
  skip_final_snapshot    = true
}

resource "aws_db_parameter_group" "weather-pgroup" {
  name   = "weather-pgroup"
  family = "postgres18"

  parameter {
    name  = "log_connections"
    value = "all"
  }
}
