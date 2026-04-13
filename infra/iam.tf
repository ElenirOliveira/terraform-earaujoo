# =========================================================
# ROLE DO AWS GLUE
# =========================================================

resource "aws_iam_role" "glue_role" {
  name = "${var.environment}-earaujo-glue-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = "sts:AssumeRole"
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

resource "aws_iam_policy" "glue_policy" {
  name = "${var.environment}-earaujo-glue-policy"

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

# =========================================================
# ROLE DA LAMBDA
# =========================================================

resource "aws_iam_role" "lambda_role" {
  name = "${var.environment}-earaujo-lambda-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = "sts:AssumeRole"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })
}

# =========================================================
# POLICY DA LAMBDA
# =========================================================

resource "aws_iam_policy" "lambda_policy" {
  name = "${var.environment}-earaujo-lambda-policy"

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

# =========================================================
# ROLE STEP FUNCTION
# =========================================================

resource "aws_iam_role" "step_function_role" {
  name = "${var.environment}-earaujo-step-function-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = "sts:AssumeRole"
        Principal = {
          Service = "states.amazonaws.com"
        }
      }
    ]
  })
}

# =========================================================
# POLICY STEP FUNCTION
# =========================================================

resource "aws_iam_policy" "step_function_policy" {
  name = "${var.environment}-earaujo-step-function-policy"

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