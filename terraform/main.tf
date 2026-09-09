provider "aws" {
  region  = "us-east-1"
  profile = "portfolio-sandbox"
}

# --- DynamoDB Tables ---

resource "aws_dynamodb_table" "tb_user_profile" {
  name         = "tb_user_profile"
  billing_mode = "PAY_PER_REQUEST" # Fundamental for zero-cost serverless architectures
  hash_key     = "user_id"

  attribute {
    name = "user_id"
    type = "S"
  }

  tags = {
    Environment = "Dev"
    Project     = "Event-Driven-Data-Pipeline"
  }
}

resource "aws_dynamodb_table" "tb_user_activity" {
  name         = "tb_user_activity"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "user_id"

  attribute {
    name = "user_id"
    type = "S"
  }

  tags = {
    Environment = "Dev"
    Project     = "Event-Driven-Data-Pipeline"
  }
}

resource "aws_dynamodb_table" "tb_execution_status" {
  name         = "tb_execution_status"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "user_id"

  attribute {
    name = "user_id"
    type = "S"
  }

  tags = {
    Environment = "Dev"
    Project     = "Event-Driven-Data-Pipeline"
  }
}
