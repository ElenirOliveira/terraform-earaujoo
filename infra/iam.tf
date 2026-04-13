# =========================================================
# ROLE DO AWS GLUE
# =========================================================
# Essa role será usada pelos jobs do Glue

resource "aws_iam_role" "glue_role" {
  name = "earaujo-glue-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = "sts:AssumeRole"

        # Serviço Glue assume essa role
        Principal = {
          Service = "glue.amazonaws.com"
        }
      }
    ]
  })
}

# =========================================================
# POLICY DO GLUE
# =========================================================
# Permissões básicas para executar jobs

resource "aws_iam_policy" "glue_policy" {
  name = "earaujo-glue-policy"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "s3:*",
          "logs:*"
        ]
        Resource = "*"
      }
    ]
  })
}

# =========================================================
# ATTACH POLICY NA ROLE
# =========================================================

resource "aws_iam_role_policy_attachment" "glue_attach" {
  role       = aws_iam_role.glue_role.name
  policy_arn = aws_iam_policy.glue_policy.arn
}

# Role responsável por executar a função lambda (coleta de dados)
resource "aws_iam_role" "lambda_role" {
  name = "earaujo-lambda-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = "sts:AssumeRole"

        # Serviço Lambda assume essa role
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })
}

# Policy da Lambda
# Permite escrever no S3 e gerar logs

resource "aws_iam_policy" "lambda_policy" {
  name = "earaujo-lambda-policy"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "s3:PutObject",
          "s3:GetObject",
          "logs:*"
        ]
        Resource = "*"
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "lambda_attach" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = aws_iam_policy.lambda_policy.arn
}

#Responsável por orquestrar Lambda + Glue

resource "aws_iam_role" "step_function_role" {
  name = "earaujo-step-function-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = "sts:AssumeRole"

        # Serviço Step Functions assume essa role
        Principal = {
          Service = "states.amazonaws.com"
        }
      }
    ]
  })
}

# Policy da Step Function
# Permite chamar Lambda e executar Glue

resource "aws_iam_policy" "step_function_policy" {
  name = "earaujo-step-function-policy"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "lambda:InvokeFunction",
          "glue:StartJobRun"
        ]
        Resource = "*"
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "step_function_attach" {
  role       = aws_iam_role.step_function_role.name
  policy_arn = aws_iam_policy.step_function_policy.arn
}

# Policy do GitHub
# Permite criar e alterar infraestrutura

resource "aws_iam_policy" "github_actions_policy" {
  name = "earaujo-github-actions-policy"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "s3:*",
          "dynamodb:*",
          "lambda:*",
          "glue:*",
          "states:*",
          "iam:*"
        ]
        Resource = "*"
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "github_attach" {
  role       = aws_iam_role.github_actions_role.name
  policy_arn = aws_iam_policy.github_actions_policy.arn
}

#
