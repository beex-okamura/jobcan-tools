import boto3
from pydantic import BaseModel

from lib.environment import get_environment

env = get_environment()

class SecretsValues(BaseModel):
    slack_verification_token: str


class Secrets():
    def __init__(self):
        session = boto3.session.Session()  # type: ignore
        self.secrets = session.client(
            service_name='secretsmanager',
            endpoint_url=env.endpoint_url,
            region_name='ap-northeast-1',
        )

    def get_secrets(self) -> SecretsValues:
        self.secrets.get_secret_value(SecretId=env.secret_name)
