resource "aws_iam_role" "jobcan-basic-lambda" {
    name = "${var.app_name}-${var.env}-basic-lambda-role"
    assume_role_policy = jsonencode({
        "Version" : "2012-10-17",
        "Statement" : [{
            "Action" : "sts:AssumeRole",
            "Principal" : {
                "Service" : "lambda.amazonaws.com"
            },
            "Effect" : "Allow",
        }]
    })
}

resource "aws_iam_role" "jobcan-scraping-lambda" {
    name = "${var.app_name}-${var.env}-scraping-lambda-role"
    assume_role_policy = jsonencode({
        "Version" : "2012-10-17",
        "Statement" : [{
            "Action" : "sts:AssumeRole",
            "Principal" : {
                "Service" : "lambda.amazonaws.com"
            },
            "Effect" : "Allow",
        }]
    })
}
