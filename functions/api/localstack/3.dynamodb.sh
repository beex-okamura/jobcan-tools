#!/bin/bash
export AWS_DEFAULT_REGION=ap-northeast-1
chmod +x /etc/localstack/init/ready.d/dynamodb/*.sh

/etc/localstack/init/ready.d/dynamodb/user-attributes.sh
