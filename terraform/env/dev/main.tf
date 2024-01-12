terraform {
    required_version = ">= 1.0.0"
    required_providers {
        aws = {
            source  = "hashicorp/aws"
            version = "~> 5.0"
        }
    }

    backend "s3" {
      region = "ap-northeast-1"
      bucket = "okamura-terraform-bucket"
      key = "jobcan-terraform/env/dev/terraform.tfstate"
      encrypt = true
    }
}

locals {
    app_name = "jobcan"
    region = "ap-northeast-1"
    env = "dev"
}

module "aws" {
    source = "../../modules/aws"
    app_name = local.app_name
    env = local.env
}
