#!/bin/bash
export AWS_DEFAULT_REGION=ap-northeast-1
awslocal secretsmanager create-secret --name jobcan-tools --secret-string file:///etc/localstack/init/ready.d/local-secrets.json
