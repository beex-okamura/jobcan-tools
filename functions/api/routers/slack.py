from fastapi import APIRouter, Header, HTTPException

from lib.environment import get_environment
from schemas.slack import SlackActionRequest, SlackActionResponse

router = APIRouter()
env = get_environment()


@router.post(
    "/slack/actions",
    response_model=SlackActionResponse | None,
)
def slack_actions(event: SlackActionRequest, x_slack_retry_num: int = Header(0)):
    if not event.bot_id or x_slack_retry_num > 0:
        return

    if env.slack_verification_token != event.token:
        raise HTTPException(status_code=401, detail="Invalid token")

    if event.type == "url_verification":
        return {"challenge": event.challenge}

    print(event)
