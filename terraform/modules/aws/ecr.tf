resource "aws_ecr_repository" "jobcan-scraping-lambda-repo" {
  name = "${var.app_name}-${var.env}-scraping-lambda"
  image_scanning_configuration {
    scan_on_push = true
  }
}

resource "aws_ecr_repository" "jobcan-tools-api-repo" {
  name = "${var.app_name}-tools-api-${var.env}"
  image_scanning_configuration {
    scan_on_push = true
  }
}

resource "aws_ecr_repository" "jobcan-tools-scraping-repo" {
  name = "${var.app_name}-tools-scraping-${var.env}"
  image_scanning_configuration {
    scan_on_push = true
  }
}