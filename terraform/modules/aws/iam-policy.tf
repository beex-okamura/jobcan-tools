resource "aws_iam_policy" "jobcan-lambda-setup" {
    name = "${var.app_name}-${var.env}-lambda-setup-policy"
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "ec2:CreateNetworkInterface",
          "ec2:DescribeNetworkInterfaces",
          "ec2:DeleteNetworkInterface"
        ]
        Effect   = "Allow"
        Resource = "*"
      },
      {
        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ]
        Effect   = "Allow"
        Resource = "*"
      }
    ]
  })
}

resource "aws_iam_policy" "jobcan-scraping-sqs-lambda-queue-policy" {
  name = "${var.app_name}-${var.env}-scraping-sqs-lambda-policy"
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "sqs:SendMessage",
          "sqs:ReceiveMessage",
          "sqs:DeleteMessage",
          "sqs:GetQueueAttributes",
        ]
        Effect = "Allow"
        Resource = [
          aws_sqs_queue.sqs_jobcan_scraping_lambda_queue.arn,
        ]
      }
    ]
  })
}

resource "aws_iam_policy" "jobcan-scraping-s3-scraping-capture-policy" {
  name = "${var.app_name}-${var.env}-scraping-s3-scraping-capture-policy"
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "s3:PutObject"
        ]
        Effect = "Allow"
        Resource = [
          "${aws_s3_bucket.bucket_scraping_capture.arn}/*",
        ]
      }
    ]
  })
}
