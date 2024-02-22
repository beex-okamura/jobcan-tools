import os
from functools import lru_cache
from pydantic_settings import BaseSettings

class Environment(BaseSettings):
    """環境変数を定義する構造体。
    """
    stage: str
    secret_name: str
    punch_work_queue_url: str
    endpoint_url: str | None


@lru_cache()
def get_environment() -> Environment:
    """環境変数を取得する。
    """
    return Environment(
        stage=os.environ.get("STAGE", "local"),
        secret_name=os.environ["SECRETS_KEY_NAME"],
        endpoint_url=os.environ.get("LOCALSTACK_URL", None),
        punch_work_queue_url=os.environ['PUNCH_WORK_QUEUE_URL']
    )
