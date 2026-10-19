from lib.slack import Slack, work_message_attribute
from lib.sqs import SQSClient
from schemas.scraping_payload import ScrapingPayload
from schemas.users import UserInfo

slack_client = Slack()


def accept_punch(user_info: UserInfo, choice_work_type: str, channel: str) -> str:
    """打刻を受けつけて SQS に送り、Slack の通知とステータスを更新する。"""
    work_type = work_message_attribute[choice_work_type]
    message = f"{work_type['name']} 処理を受けつけました"

    slack_client.send_message(channel, message)

    sqs_payload = ScrapingPayload.model_validate(
        {
            **user_info.model_dump(),
            "choice_work_type": choice_work_type,
            "channel": channel,
        }
    )
    SQSClient().send_punch_clock_message(sqs_payload)

    user_slack = Slack(token=user_info.slack_access_token)

    for ch in user_info.send_punch_channels or []:
        user_slack.send_message(ch, work_type["icon"])

    user_slack.change_status(work_type["name"], work_type["icon"])

    return message
