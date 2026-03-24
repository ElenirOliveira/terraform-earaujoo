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