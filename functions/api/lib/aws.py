import boto3  # type: ignore

from lib.environment import get_environment

env = get_environment()
session = boto3.session.Session()  # type: ignore

secrets_client = session.client(
    service_name="secretsmanager",
    endpoint_url=env.endpoint_url,
    region_name="ap-northeast-1",
)
