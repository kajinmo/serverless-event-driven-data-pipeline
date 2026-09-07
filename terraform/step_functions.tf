resource "aws_iam_role" "sfn_exec_role" {
  name = "sfn_exec_role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "states.amazonaws.com"
        }
      }
    ]
  })

  inline_policy {
    name = "sfn_policy"
    policy = jsonencode({
      Version = "2012-10-17"
      Statement = [
        {
          Action = [
            "dynamodb:GetItem"
          ]
          Effect   = "Allow"
          Resource = [
            aws_dynamodb_table.tb_user_profile.arn,
            aws_dynamodb_table.tb_user_activity.arn
          ]
        },
        {
          Action = [
            "lambda:InvokeFunction"
          ]
          Effect   = "Allow"
          Resource = [
            aws_lambda_function.data_consolidation_lambda.arn
          ]
        }
      ]
    })
  }
}

resource "aws_sfn_state_machine" "data_consolidation_sfn" {
  name     = "DataConsolidationStateMachine"
  role_arn = aws_iam_role.sfn_exec_role.arn

  definition = templatefile("${path.module}/state_machine.asl.json", {
    lambda_arn = aws_lambda_function.data_consolidation_lambda.arn
  })
}
