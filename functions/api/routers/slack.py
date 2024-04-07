from fastapi import APIRouter, Header, HTTPException

from lib.secrets import get_secrets
from lib.slack import choice_work_message
from lib.sqs import SQSClient
from routers.logging import TimedRoute
from schemas.slack import SlackActionRequest, SlackActionResponse
from services.users import Users

router = APIRouter(route_class=TimedRoute)
secrets = get_secrets()


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
    choice_work_message(event.text)

    user_info = Users.get_user(event.user)

    SQSClient().send_punch_clock_message(user_info)
