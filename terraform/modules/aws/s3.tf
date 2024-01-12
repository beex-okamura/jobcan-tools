resource "aws_s3_bucket" "bucket-serverless-deploy" {
    bucket = "${var.app_name}-serverless-deploy-${var.env}"
}

resource "aws_s3_bucket" "bucket_scraping_capture" {
  bucket = "${var.app_name}-${var.env}-scraping-capture"
}

resource "aws_s3_bucket_server_side_encryption_configuration" "bucket_scraping_capture" {
  bucket = aws_s3_bucket.bucket_scraping_capture.id
  rule {
    bucket_key_enabled = true
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_public_access_block" "bucket_scraping_capture" {
  bucket = aws_s3_bucket.bucket_scraping_capture.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_versioning" "bucket_scraping_capture" {
  bucket = aws_s3_bucket.bucket_scraping_capture.id

  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_lifecycle_configuration" "bucket_scraping_capture" {
  bucket     = aws_s3_bucket.bucket_scraping_capture.id
  depends_on = [aws_s3_bucket_versioning.bucket_scraping_capture]

  rule {
    id     = "delete-versioning-files"
    status = "Enabled"

    noncurrent_version_expiration {
      newer_noncurrent_versions = "20"
      noncurrent_days           = 60
    }
  }
}