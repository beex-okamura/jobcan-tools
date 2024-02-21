#!/bin/bash
export AWS_DEFAULT_REGION=ap-northeast-1
awslocal sqs create-queue --queue-name jobcan-local-scraping-lambda-queue
