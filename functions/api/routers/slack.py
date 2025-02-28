from fastapi import APIRouter, Header, HTTPException

from lib.secrets import get_secrets
from lib.slack import Slack, choice_work_message, work_message_attribute
from lib.sqs import SQSClient
from routers.logging import TimedRoute
from schemas.scraping_payload import ScrapingPayload
from schemas.slack import (
    SlackActionRequest,
    SlackActionResponse,
    SlackSendMessageRequest,
)
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
    work_type = work_message_attribute[choice_work_type]

    user_info = Users.get_user(event.user)

    slack_client.send_message(
        event.channel, f"{work_type["name"]} 処理を受けつけました"
    )

    sqs_payload: ScrapingPayload = ScrapingPayload.model_validate(
        {
            **user_info.model_dump(),
            "choice_work_type": choice_work_type,
            "channel": event.channel,
        }
    )

    SQSClient().send_punch_clock_message(sqs_payload)

    user_slack = Slack(token=user_info.slack_access_token)

    if user_info.send_punch_channels and len(user_info.send_punch_channels) > 0:
        for channel in user_info.send_punch_channels:
            user_slack.send_message(channel, work_type["icon"])

    user_slack.change_status(work_type["name"], work_type["icon"])


@router.post(
    "/slack/message",
)
def send_message(request: SlackSendMessageRequest):
    if secrets.SLACK_VERIFICATION_TOKEN != request.token:
        raise HTTPException(status_code=401, detail="Invalid token")

    slack_client.send_message(request.channel, request.text)
