module "lambda_function" {
  source = "terraform-aws-modules/lambda/aws"

  function_name = var.lambda_function_earaujo
  description   = "Lambda que processa dataset de filmes"
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


# S3 BUCKET (DATA LAKE)

resource "aws_s3_bucket" "data_lake" {
  bucket = var.s3_bucket_earaujoo

  tags = {
    Name        = "earaujo-data-lake"
    Environment = var.environment
  }
}


#  UPLOAD DO DATASET (CSV)

resource "aws_s3_object" "movies_csv" {
  bucket = aws_s3_bucket.data_lake.id
  key    = "LZ/movies/global_movies.csv"
  source = "../src/data/global_movies.csv"

  etag = filemd5("../src/data/global_movies.csv")
}

# GLUE DATABASE

resource "aws_glue_catalog_database" "movies_database" {
  name = var.glue_database_name
}

# GLUE CATALOG TABLE

resource "aws_glue_catalog_table" "movies_table" {
  name          = var.glue_table_name
  database_name = aws_glue_catalog_database.movies_database.name

  table_type = "EXTERNAL_TABLE"

  parameters = {
    "classification" = "parquet"
    "typeOfData"     = "file"
  }

  storage_descriptor {
    location      = "s3://${aws_s3_bucket.data_lake.bucket}/SOR/movies/"
    input_format  = "org.apache.hadoop.hive.ql.io.parquet.MapredParquetInputFormat"
    output_format = "org.apache.hadoop.hive.ql.io.parquet.MapredParquetOutputFormat"

    ser_de_info {
      name                  = "ParquetSerDe"
      serialization_library = "org.apache.hadoop.hive.ql.io.parquet.serde.ParquetHiveSerDe"

      parameters = {
        "serialization.format" = "1"
      }
    }

    columns {
      name = "movie_id"
      type = "bigint"
    }
    columns {
      name = "title"
      type = "string"
    }
    columns {
      name = "release_year"
      type = "int"
    }
    columns {
      name = "decade"
      type = "int"
    }
    columns {
      name = "runtime_min"
      type = "int"
    }
    columns {
      name = "genre"
      type = "string"
    }
    columns {
      name = "subgenre"
      type = "string"
    }
    columns {
      name = "director"
      type = "string"
    }
    columns {
      name = "lead_actor"
      type = "string"
    }
    columns {
      name = "lead_actress"
      type = "string"
    }
    columns {
      name = "country"
      type = "string"
    }
    columns {
      name = "language"
      type = "string"
    }
    columns {
      name = "imdb_rating"
      type = "double"
    }
    columns {
      name = "votes"
      type = "bigint"
    }
    columns {
      name = "budget_million"
      type = "double"
    }
    columns {
      name = "marketing_budget_million"
      type = "double"
    }
    columns {
      name = "revenue_million"
      type = "double"
    }
    columns {
      name = "roi_pct"
      type = "double"
    }
    columns {
      name = "popularity_score"
      type = "double"
    }
    columns {
      name = "metascore"
      type = "int"
    }
    columns {
      name = "audience_score"
      type = "int"
    }
    columns {
      name = "streaming_platform"
      type = "string"
    }
    columns {
      name = "award_nominations"
      type = "int"
    }
    columns {
      name = "award_wins"
      type = "int"
    }
    columns {
      name = "top_100_prob"
      type = "double"
    }
    columns {
      name = "blockbuster_flag"
      type = "boolean"
    }
    columns {
      name = "franchise_flag"
      type = "boolean"
    }
  }
}

#  SCRIPTS GLUE

resource "aws_s3_object" "lz_to_sor_script" {
  bucket = aws_s3_bucket.data_lake.id
  key    = "jobs/lz_to_sor.py"
  source = "../src/glue_jobs/lz_to_sor.py"

  etag = filemd5("../src/glue_jobs/lz_to_sor.py")
}

resource "aws_s3_object" "sor_to_sot_script" {
  bucket = aws_s3_bucket.data_lake.id
  key    = "jobs/sor_to_sot.py"
  source = "../src/glue_jobs/sor_to_sot.py"

  etag = filemd5("../src/glue_jobs/sor_to_sot.py")
}

resource "aws_s3_object" "sot_to_spec_script" {
  bucket = aws_s3_bucket.data_lake.id
  key    = "jobs/sot_to_spec.py"
  source = "../src/glue_jobs/sot_to_spec.py"

  etag = filemd5("../src/glue_jobs/sot_to_spec.py")
}

# GLUE JOBS

resource "aws_glue_job" "lz_to_sor" {
  name        = var.glue_job_lz_to_sor
  description = "LZ → SOR (movies)"

  role_arn     = aws_iam_role.glue_role.arn
  glue_version = "5.0"

  number_of_workers = 2
  worker_type       = "G.1X"

  command {
    script_location = "s3://${aws_s3_bucket.data_lake.bucket}/jobs/lz_to_sor.py"
    name            = "glueetl"
    python_version  = "3"
  }

  default_arguments = {
    "--ENV"    = var.environment
    "--BUCKET" = var.s3_bucket_earaujoo
  }

  tags = {
    Environment = var.environment
  }
}

resource "aws_glue_job" "sor_to_sot" {
  name         = var.glue_job_sor_to_sot
  role_arn     = aws_iam_role.glue_role.arn
  glue_version = "5.0"

  command {
    script_location = "s3://${aws_s3_bucket.data_lake.bucket}/jobs/sor_to_sot.py"
    name            = "glueetl"
    python_version  = "3"
  }

  default_arguments = {
    "--ENV"    = var.environment
    "--BUCKET" = var.s3_bucket_earaujoo
  }

  tags = {
    Environment = var.environment
  }
}

resource "aws_glue_job" "sot_to_spec" {
  name         = var.glue_job_sot_to_spec
  role_arn     = aws_iam_role.glue_role.arn
  glue_version = "5.0"
  command {
    script_location = "s3://${aws_s3_bucket.data_lake.bucket}/jobs/sot_to_spec.py"
    name            = "glueetl"
    python_version  = "3"
  }

  default_arguments = {
    "--ENV"    = var.environment
    "--BUCKET" = var.s3_bucket_earaujoo
  }

  tags = {
    Environment = var.environment
  }
}

# STEP FUNCTION (ORQUESTRAÇÃO)

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
