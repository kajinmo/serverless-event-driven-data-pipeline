data "archive_file" "lambda_zip" {
  type        = "zip"
  source_dir  = "../src/lambda_function"
  output_path = "lambda_function.zip"
}

resource "aws_iam_role" "lambda_exec_role" {
  name = "lambda_exec_role"

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

resource "aws_lambda_function" "data_consolidation_lambda" {
  filename         = data.archive_file.lambda_zip.output_path
  function_name    = "DataConsolidationLambda"
  role             = aws_iam_role.lambda_exec_role.arn
  handler          = "handler.lambda_handler"
  runtime          = "python3.12"
  timeout          = 15
  source_code_hash = data.archive_file.lambda_zip.output_base64sha256

}
