resource "aws_sqs_queue" "sqs_jobcan_scraping_lambda_queue_dead_letters" {
  name                       = "${var.app_name}-${var.env}-scraping-lambda-queue-dead-letters"
  fifo_queue                 = false
  delay_seconds              = 0
  max_message_size           = 1024 * 256
  message_retention_seconds  = 60 * 60 * 24 * 14
  receive_wait_time_seconds  = 0
  visibility_timeout_seconds = 30
  policy                     = null
  redrive_policy             = null
}

resource "aws_sqs_queue" "sqs_jobcan_scraping_lambda_queue" {
  name                       = "${var.app_name}-${var.env}-scraping-lambda-queue"
  fifo_queue                 = false
  delay_seconds              = 0
  max_message_size           = 1024 * 256
  message_retention_seconds  = 60 * 60 * 24 * 14
  receive_wait_time_seconds  = 0
  visibility_timeout_seconds = 300
  policy                     = null
  redrive_policy             = <<EOF
{
  "deadLetterTargetArn": "${aws_sqs_queue.sqs_jobcan_scraping_lambda_queue_dead_letters.arn}",
  "maxReceiveCount": 5
}
EOF
}