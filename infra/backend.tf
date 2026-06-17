terraform {
  backend "s3" {
    bucket         = "weather-prediction-terraform-state"
    key            = "weather_prediction/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform-state-lock"
  }
}