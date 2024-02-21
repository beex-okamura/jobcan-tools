resource "aws_secretsmanager_secret" "jobcan-secrets" {
  name = "${var.app_name}-${var.env}-secrets"
}
