resource "aws_dynamodb_table" "jobcan_user_atttributes" {
    name           = "${var.app_name}-${var.env}-user-atttributes"
    billing_mode   = "PAY_PER_REQUEST"
    hash_key       = "user_id"
    attribute {
        name = "user_id"
        type = "S"
    }
}
