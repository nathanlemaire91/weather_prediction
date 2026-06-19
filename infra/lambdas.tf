resource "aws_iam_role" "lambda_role" {
  name = "weather-prediction-lambda-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "lambda_basic_execution" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_iam_role_policy" "lambda_rds_access" {
  name = "lambda-rds-access"
  role = aws_iam_role.lambda_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "rds-db:connect",
          "rds:*"
        ]
        Resource = "arn:aws:rds:*:*:db/*"
      }
    ]
  })
}

resource "aws_iam_role_policy" "lambda_secretsmanager_access" {
  name = "lambda-secretsmanager-access"
  role = aws_iam_role.lambda_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "secretsmanager:GetSecretValue",
          "secretsmanager:DescribeSecret",
          "secretsmanager:ListSecrets",
          "secretsmanager:ListSecretVersionIds"
        ]
        Resource = "arn:aws:secretsmanager:*:*:secret:*"
      },
      {
        Effect = "Allow"
        Action = [
          "kms:Decrypt"
        ]
        Resource = "*"
      }
    ]
  })
}

resource "aws_lambda_function" "weather_prediction" {
  filename      = "weather-prediction.zip"
  function_name = "weather-prediction"
  role          = aws_iam_role.lambda_role.arn
  handler       = "index.handler"
  runtime       = "python3.12"

  s3_bucket = "weather-prediction-bucket-dev"
  s3_key    = "lambdas/weather-prediction.zip"

  environment {
    variables = {
      RDS_HOST = "weather-rds.cw7yw8aieuh1.us-east-1.rds.amazonaws.com"
      RDS_PORT = "5432"
      RDS_DB_NAME = "weather-rds"
      RDS_USERNAME = "edu"
      S3_BUCKET_NAME = "weather-prediction-bucket-dev"
      S3_SCALER_KEY = "scalers/scaler"
      S3_MODEL_KEY = "models/lstm_weather_model"
    }
  }
}

resource "aws_lambda_permission" "allow_apigateway" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.weather_prediction.function_name
  principal     = "apigateway.amazonaws.com"
}
