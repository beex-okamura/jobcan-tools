from pydantic import BaseModel

from lib.environment import get_environment
from lib.aws import secrets_client

env = get_environment()

class SecretsValues(BaseModel):
    SLACK_VERIFICATION_TOKEN: str
    SLACK_SEND_TOKEN: str

def get_secrets():
    return SecretsValues.model_validate_json(
        secrets_client.get_secret_value(SecretId=env.secret_name)["SecretString"]
    )
