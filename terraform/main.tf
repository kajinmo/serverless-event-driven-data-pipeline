provider "aws" {
  region     = "us-east-1"
  access_key = "test"
  secret_key = "test"

  # Mandatory flags to bypass authentication in the real cloud
  skip_credentials_validation = true
  skip_metadata_api_check     = true
  skip_requesting_account_id  = true

  # Redirect APIs to the Floci container
  endpoints {
    dynamodb      = "http://localhost:4566"
    stepfunctions = "http://localhost:4566"
    lambda        = "http://localhost:4566"
    iam           = "http://localhost:4566"
  }
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
