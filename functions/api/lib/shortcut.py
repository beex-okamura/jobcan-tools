import hashlib
import hmac


def issue_shortcut_token(signing_secret: str, user_id: str) -> str:
    """Slack の user_id に紐づくショートカット用トークンを発行する。"""
    return hmac.new(
        signing_secret.encode(), user_id.encode(), hashlib.sha256
    ).hexdigest()


def verify_shortcut_token(signing_secret: str, user_id: str, token: str) -> bool:
    return hmac.compare_digest(issue_shortcut_token(signing_secret, user_id), token)
