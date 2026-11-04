from fastapi import APIRouter, Header, HTTPException

from lib.secrets import get_secrets
from lib.slack import Slack, choice_work_message
from routers.logging import TimedRoute
from schemas.slack import (
    SlackActionRequest,
    SlackActionResponse,
    SlackSendMessageRequest,
)
from services.punch import accept_punch
from services.users import Users

router = APIRouter(route_class=TimedRoute)
secrets = get_secrets()
slack_client = Slack()


@router.post(
    "/slack/actions",
    response_model=SlackActionResponse | None,
)
def slack_actions(request: SlackActionRequest, x_slack_retry_num: int = Header(0)):
    if secrets.SLACK_VERIFICATION_TOKEN != request.token:
        raise HTTPException(status_code=401, detail="Invalid token")

    if request.type == "url_verification":
        return {"challenge": request.challenge}

    if request.bot_id or x_slack_retry_num > 0:
        return

    event = request.event

    if event is None or event.bot_id is not None:
        return

    choice_work_type = choice_work_message(event.text)

    user_info = Users.get_user(event.user)

    # 処理結果は打刻したチャンネルではなく、ボットからユーザーへの DM に通知する
    accept_punch(user_info, choice_work_type, event.user)


@router.post(
    "/slack/message",
)
def send_message(request: SlackSendMessageRequest):
    if secrets.SLACK_VERIFICATION_TOKEN != request.token:
        raise HTTPException(status_code=401, detail="Invalid token")

    slack_client.send_message(request.channel, request.text)
