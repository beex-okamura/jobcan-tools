table_count=$(awslocal dynamodb list-tables --query 'length(TableNames[?@==`jobcan-local-user-attributes`])')

if [ $table_count -eq 0 ]; then
  # create localstack master table
  awslocal dynamodb create-table \
  --table-name jobcan-local-user-attributes \
  --attribute-definitions AttributeName=user_id,AttributeType=S \
  --key-schema AttributeName=user_id,KeyType=HASH \
  --billing-mode PAY_PER_REQUEST
fi

awslocal dynamodb put-item \
  --table-name jobcan-local-user-attributes \
  --item '{
    "user_id": {"S": "UGL5J91HV"},
    "jobcan_user_id": {"S": "UGL5J91HV"},
    "jobcan_password": {"S": "password"}
  }'
