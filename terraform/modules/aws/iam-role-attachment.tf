resource "aws_iam_role_policy_attachment" "jobcan-basic-lambda" {
  role       = aws_iam_role.jobcan-basic-lambda.name
  policy_arn = aws_iam_policy.jobcan-lambda-setup.arn 
}

resource "aws_iam_role_policy_attachment" "jobcan-secrets-manager-lambda" {
  role       = aws_iam_role.jobcan-basic-lambda.name
  policy_arn = aws_iam_policy.jobcan-secerts-manager-policy.arn
}

resource "aws_iam_role_policy_attachment" "jobcan-scraping-sqs-lambda" {
  role       = aws_iam_role.jobcan-basic-lambda.name
  policy_arn = aws_iam_policy.jobcan-scraping-sqs-lambda-queue-policy.arn
}

resource "aws_iam_role_policy_attachment" "jobcan-scraping-s3-scraping-capture" {
  role       = aws_iam_role.jobcan-basic-lambda.name
  policy_arn = aws_iam_policy.jobcan-scraping-s3-scraping-capture-policy.arn  
}