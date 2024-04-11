resource "aws_iam_role_policy_attachment" "jobcan-basic-lambda" {
  role       = aws_iam_role.jobcan-basic-lambda.name
  policy_arn = aws_iam_policy.jobcan-lambda-setup.arn 
}

resource "aws_iam_role_policy_attachment" "jobcan-secrets-manager-lambda" {
  role       = aws_iam_role.jobcan-basic-lambda.name
  policy_arn = aws_iam_policy.jobcan-secerts-manager-policy.arn
}

resource "aws_iam_role_policy_attachment" "jobcan-scraping-lambda" {
  role = aws_iam_role.jobcan-scraping-lambda.name
  policy_arn = aws_iam_policy.jobcan-lambda-setup.arn
}

resource "aws_iam_role_policy_attachment" "jobcan-api-lambda" {
  role = aws_iam_role.jobcan-api-lambda.name
  policy_arn = aws_iam_policy.jobcan-lambda-setup.arn
}

resource "aws_iam_role_policy_attachment" "jobcan-api-user-attributes" {
  role = aws_iam_role.jobcan-api-lambda.name
  policy_arn = aws_iam_policy.jobcan-api-read-user-attributes-policy.arn  
}

resource "aws_iam_role_policy_attachment" "jobcan-api-sqs" {
  role = aws_iam_role.jobcan-api-lambda.name
  policy_arn = aws_iam_policy.jobcan-scraping-sqs-lambda-queue-policy.arn  
}

resource "aws_iam_role_policy_attachment" "jobcan-api-secrets" {
  role = aws_iam_role.jobcan-api-lambda.name
  policy_arn = aws_iam_policy.jobcan-secerts-manager-policy.arn
}

resource "aws_iam_role_policy_attachment" "jobcan-scraping-secrets-lambda" {
  role       = aws_iam_role.jobcan-scraping-lambda.name
  policy_arn = aws_iam_policy.jobcan-secerts-manager-policy.arn
}

resource "aws_iam_role_policy_attachment" "jobcan-scraping-sqs-lambda" {
  role       = aws_iam_role.jobcan-scraping-lambda.name
  policy_arn = aws_iam_policy.jobcan-scraping-sqs-lambda-queue-policy.arn
}

resource "aws_iam_role_policy_attachment" "jobcan-scraping-s3-scraping-capture" {
  role       = aws_iam_role.jobcan-scraping-lambda.name
  policy_arn = aws_iam_policy.jobcan-scraping-s3-scraping-capture-policy.arn  
}

resource "aws_iam_role_policy_attachment" "jobcan-scraping-kms-lambda" {
  role = aws_iam_role.jobcan-scraping-lambda.name
  policy_arn = aws_iam_policy.jobcan-kms-policy.arn
}
