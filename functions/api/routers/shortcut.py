import logging

from fastapi import APIRouter, Header, HTTPException
from pynamodb.exceptions import DoesNotExist

from lib.secrets import get_secrets
from lib.shortcut import verify_shortcut_token
from lib.slack import work_message_attribute
from schemas.shortcut import ShortcutPunchRequest, ShortcutPunchResponse
from services.punch import accept_punch
from services.users import Users

# トークンを含むヘッダーをログに出さないよう、TimedRoute は使わない
router = APIRouter()
secrets = get_secrets()

# API 全体ではログのハンドラを設定していないので、このルーターだけ標準出力に出す
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
if not logger.handlers:
    logger.addHandler(logging.StreamHandler())

# 「出勤」などの表示名でも clock_in などのキーでも受けつける
WORK_TYPE_BY_NAME = {v["name"]: k for k, v in work_message_attribute.items()}


@router.post("/shortcut/punch", response_model=ShortcutPunchResponse)
def shortcut_punch(request: ShortcutPunchRequest, authorization: str = Header("")):
    if secrets.SHORTCUT_SIGNING_SECRET is None:
        raise HTTPException(status_code=503, detail="Shortcut is not configured")

    token = authorization.removeprefix("Bearer ").strip()
    if not verify_shortcut_token(
        secrets.SHORTCUT_SIGNING_SECRET, request.user_id, token
    ):
        logger.warning("Shortcut rejected: invalid token, user_id=%s", request.user_id)
        raise HTTPException(status_code=401, detail="Invalid token")

    choice_work_type = WORK_TYPE_BY_NAME.get(request.work_type, request.work_type)
    if choice_work_type not in work_message_attribute:
        logger.warning("Shortcut rejected: invalid work_type=%s", request.work_type)
        raise HTTPException(status_code=400, detail="Invalid work_type")

    try:
        user_info = Users.get_user(request.user_id)
    except DoesNotExist:
        logger.warning("Shortcut rejected: unknown user_id=%s", request.user_id)
        raise HTTPException(status_code=404, detail="User not found")

    logger.info(
        "Shortcut request: work_type=%s, user_id=%s", choice_work_type, request.user_id
    )

    # 処理結果はボットからユーザーへの DM に通知する
    message = accept_punch(user_info, choice_work_type, request.user_id)

    return ShortcutPunchResponse(message=message)
