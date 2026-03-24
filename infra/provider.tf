#provider "aws" {
  #region = "us-east-1"
#}

provider "aws" {
  region = var.environment == "prd" ? "us-east-1" : "us-east-1"
}