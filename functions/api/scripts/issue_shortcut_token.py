"""iPhone ショートカット用のトークンを発行する。

使い方:
    SECRETS_KEY_NAME=jobcan-dev-secrets python scripts/issue_shortcut_token.py <Slack user_id>
"""

import json
import os
import sys

import boto3  # type: ignore

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from lib.shortcut import issue_shortcut_token  # noqa: E402


def main():
    if len(sys.argv) != 2:
        sys.exit("usage: issue_shortcut_token.py <Slack user_id>")

    client = boto3.client("secretsmanager", region_name="ap-northeast-1")
    secret = json.loads(
        client.get_secret_value(SecretId=os.environ["SECRETS_KEY_NAME"])["SecretString"]
    )
    signing_secret = secret.get("SHORTCUT_SIGNING_SECRET")
    if not signing_secret:
        sys.exit("SHORTCUT_SIGNING_SECRET is not set in the secret")

    print(issue_shortcut_token(signing_secret, sys.argv[1]))


if __name__ == "__main__":
    main()
