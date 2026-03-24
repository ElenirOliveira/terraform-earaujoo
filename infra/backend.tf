terraform {
  backend "s3" {
    bucket         = "earaujo-terraform-state"
    key            = "infra/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "earaujo-terraform-lock"
    encrypt        = true
  }
}