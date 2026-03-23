import logging

from slack_sdk import WebClient

from lib.slack import Slack, work_message_attribute
from lib.sqs import SQSClient
from schemas.alexa import AlexaRequest
from schemas.scraping_payload import ScrapingPayload
from services.users import Users

INTENT_TO_WORK_TYPE = {
    "ClockInIntent": "clock_in",
    "ClockOutIntent": "clock_out",
    "GoOutIntent": "go_out",
    "ReturnedIntent": "returned",
    "GoOfficeInIntent": "go_office_in",
    "LeaveOfficeIntent": "leave_office_in",
}

LAUNCH_MESSAGE = "出勤、退勤、外出、再入、出社、退社のいずれかを話しかけてください"
NOTIFICATION_CHANNEL = "C031M12GJPK"

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

slack_client = Slack()


def _get_slack_user_id(access_token: str) -> str:
    client = WebClient(token=access_token)
    response = client.users_identity()
    return response["user"]["id"]


def _build_response(speech_text: str, should_end_session: bool = True) -> dict:
    return {
        "version": "1.0",
        "response": {
            "outputSpeech": {
                "type": "PlainText",
                "text": speech_text,
            },
            "shouldEndSession": should_end_session,
        },
    }


def alexa_handler(event: dict, context) -> dict:
    alexa_request = AlexaRequest.model_validate(event)
    request_type = alexa_request.request.type

    if request_type == "LaunchRequest":
        return _build_response(LAUNCH_MESSAGE, should_end_session=False)

    if request_type == "SessionEndedRequest":
        return _build_response("")

    if request_type != "IntentRequest":
        return _build_response("")

    intent = alexa_request.request.intent
    if intent is None:
        return _build_response("インテントを認識できませんでした")

    choice_work_type = INTENT_TO_WORK_TYPE.get(intent.name)
    if choice_work_type is None:
        return _build_response("対応していない操作です")

    access_token = alexa_request.session.user.accessToken
    if access_token is None:
        return _build_response("アカウントリンクを設定してください")

    user_id = _get_slack_user_id(access_token)
    logger.info("Alexa request: intent=%s, user_id=%s", intent.name, user_id)
    user_info = Users.get_user(user_id)

    if not user_info.send_punch_channels or len(user_info.send_punch_channels) == 0:
        return _build_response("通知チャネルが設定されていません")

    channel = NOTIFICATION_CHANNEL
    work_type = work_message_attribute[choice_work_type]

    slack_client.send_message(channel, f"{work_type['name']} 処理を受けつけました")

    sqs_payload = ScrapingPayload.model_validate(
        {
            **user_info.model_dump(),
            "choice_work_type": choice_work_type,
            "channel": channel,
        }
    )
    SQSClient().send_punch_clock_message(sqs_payload)

    user_slack = Slack(token=user_info.slack_access_token)

    for ch in user_info.send_punch_channels:
        user_slack.send_message(ch, work_type["icon"])

    user_slack.change_status(work_type["name"], work_type["icon"])

    return _build_response(f"{work_type['name']}処理を受けつけました")
