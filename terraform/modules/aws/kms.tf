resource "aws_kms_key" "kms_custmer_key" {
    description = "Customer key for ${var.app_name} ${var.env}"
}

resource "aws_kms_alias" "kms_custmer_key" {
    name = "alias/${var.app_name}-customer-key-${var.env}"
    target_key_id = aws_kms_key.kms_custmer_key.id
}