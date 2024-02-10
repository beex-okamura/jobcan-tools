from functools import lru_cache
import os
from pydantic_settings import BaseSettings

class Environment(BaseSettings):
    """環境変数を定義する構造体。
    """
    slack_verification_token: str
    stage: str


@lru_cache()
def get_environment() -> Environment:
    """環境変数を取得する。
    """
    return Environment(
        slack_verification_token=os.environ["SLACK_VERIFICATION_TOKEN"],
        stage=os.environ.get("STAGE", "local")
    )
