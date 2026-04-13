variable "environment" {
  description = "Ambiente de execução (dev ou prd)"
  type        = string

  validation {
    condition     = contains(["dev", "prd"], var.environment)
    error_message = "O ambiente deve ser 'dev' ou 'prd'."
  }
}
#variable "region" {
  #description = "Região AWS"
  #type        = string
#}

variable "lambda_function_earaujo" {
  description = "Nome da função AWS Lambda"
  type        = string
}

variable "s3_bucket_earaujoo" {
  description = "Nome do bucket S3 para armazenamento de dados"
  type        = string
}

variable "glue_job_lz_to_sor" {
  description = "Job Glue LZ → Sor"
  type        = string
}

variable "glue_job_sor_to_sot" {
  description = "Job Glue Sor → SOT"
  type        = string
}

variable "glue_job_sot_to_spec" {
  description = "Job Glue SOT → SPEC"
  type        = string
}

variable "step_function_tform" {
  description = "Nome da AWS Step Function responsável pela orquestração"
  type        = string
}