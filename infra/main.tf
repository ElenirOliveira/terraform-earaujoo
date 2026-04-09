module "lambda_function" {
  source = "terraform-aws-modules/lambda/aws"

  function_name = var.lambda_function_earaujo
  description   = "Lambda que consulta"
  handler       = "index.lambda_handler"
  runtime       = "python3.12"
  timeout       = 120
  memory_size   = 512

  create_role = false
  lambda_role = aws_iam_role.lambda_role.arn

  environment_variables = {
    BUCKET_NAME = var.s3_bucket_earaujoo
  }

  layers = ["arn:aws:lambda:us-east-1:336392948345:layer:AWSSDKPandas-Python312:22"]

  source_path             = "../src/lambda"
  ignore_source_code_hash = true

  tags = {
    Name        = "earaujo-etl"
    Environment = var.environment
  }
}

resource "aws_s3_bucket" "data_lake" {
  bucket = var.s3_bucket_earaujoo

  tags = {
    Name        = "earaujo-data-lake"
    Environment = var.environment
  }
}

resource "aws_s3_object" "lz_to_sor_script" {
  bucket = aws_s3_bucket.data_lake.id
  key    = "jobs/lz_to_sor.py"
  source = "../src/glue_jobs/lz_to_sor.py"
}

resource "aws_glue_job" "lz_to_sor" {
  name        = var.glue_job_lz_to_sor
  description = "Processamento da camada LZ para SOR"

  # CORREÇÃO: usa a role criada no Terraform
  role_arn = aws_iam_role.glue_role.arn

  glue_version = "5.0"

  number_of_workers = 2
  worker_type       = "G.1X"

  command {
    script_location = "s3://${aws_s3_bucket.data_lake.bucket}/jobs/lz_to_sor.py"
    name            = "glueetl"
    python_version  = "3"
  }

  tags = {
    Environment = var.environment
  }
}

resource "aws_s3_object" "sor_to_sot_script" {
  bucket = aws_s3_bucket.data_lake.id
  key    = "jobs/sor_to_sot.py"
  source = "../src/glue_jobs/sor_to_sot.py"
}

resource "aws_glue_job" "sor_to_sot" {
  name = var.glue_job_sor_to_sot

  # CORREÇÃO: usa a role criada no Terraform
  role_arn = aws_iam_role.glue_role.arn

  command {
    script_location = "s3://${aws_s3_bucket.data_lake.bucket}/jobs/sor_to_sot.py"
    name            = "glueetl"
  }

  tags = {
    Environment = var.environment
  }
}

resource "aws_s3_object" "sot_to_spec_script" {
  bucket = aws_s3_bucket.data_lake.id
  key    = "jobs/sot_to_spec.py"
  source = "../src/glue_jobs/sot_to_spec.py"
}

resource "aws_glue_job" "sot_to_spec" {
  name = var.glue_job_sot_to_spec

  # CORREÇÃO: usa a role criada no Terraform
  role_arn = aws_iam_role.glue_role.arn

  command {
    script_location = "s3://${aws_s3_bucket.data_lake.bucket}/jobs/sot_to_spec.py"
    name            = "glueetl"
  }

  tags = {
    Environment = var.environment
  }
}

module "step_function" {
  source = "terraform-aws-modules/step-functions/aws"

  name = var.step_function_tform

  create_role       = false
  use_existing_role = true
  role_arn          = aws_iam_role.step_function_role.arn

  definition = <<EOF
{
  "StartAt": "Lambda",
  "States": {
    "Lambda": {
      "Type": "Task",
      "Resource": "arn:aws:states:::lambda:invoke",
      "Parameters": {
        "FunctionName": "${var.lambda_function_earaujo}"
      },
      "Next": "LZ to SOR"
    },
    "LZ to SOR": {
      "Type": "Task",
      "Resource": "arn:aws:states:::glue:startJobRun.sync",
      "Parameters": {
        "JobName": "${aws_glue_job.lz_to_sor.name}"
      },
      "Next": "SOR to SOT"
    },
    "SOR to SOT": {
      "Type": "Task",
      "Resource": "arn:aws:states:::glue:startJobRun.sync",
      "Parameters": {
        "JobName": "${aws_glue_job.sor_to_sot.name}"
      },
      "Next": "SOT to SPEC"
    },
    "SOT to SPEC": {
      "Type": "Task",
      "Resource": "arn:aws:states:::glue:startJobRun.sync",
      "Parameters": {
        "JobName": "${aws_glue_job.sot_to_spec.name}"
      },
      "End": true
    }
  }
}
EOF

  tags = {
    Name        = "earaujo-orchestrator"
    Environment = var.environment
  }
}
