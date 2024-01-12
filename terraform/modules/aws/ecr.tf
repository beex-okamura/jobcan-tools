resource "aws_ecr_repository" "jobcan-scraping-lambda-repo" {
  name = "${var.app_name}-${var.env}-scraping-lambda"
  image_scanning_configuration {
    scan_on_push = true
  }
}