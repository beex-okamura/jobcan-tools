import re

from slack_sdk import WebClient

from lib.secrets import get_secrets

clock_in_match = re.compile("^(出勤|:remote-syusya:|ws|syusya).*")
clock_out_match = re.compile("^(退勤|:remote-taisya:|wt|taisya).*")
go_out_match = re.compile("^(外出|:gaisyutsu:|go|gaisyutsu).*")
returned_match = re.compile("^(再入|:sainyu:|gr|sainyu).*")

work_message_type = {
    "clock_in": "出勤",
    "clock_out": "退勤",
    "go_out": "外出",
    "returned": "再入",
}

secrets = get_secrets()

class Slack:
    def __init__(self) -> None:
        self.slack = WebClient(token=secrets.SLACK_BOT_USER_TOKEN)

    def send_message(self, channel: str, message: str):
        self.slack.chat_postMessage(channel=channel, text=message)


def choice_work_message(message: str):
    if clock_in_match.match(message):
        return "clock_in"
    elif clock_out_match.match(message):
        return "clock_out"
    elif go_out_match.match(message):
        return "go_out"
    elif returned_match.match(message):
        return "returned"

    raise ValueError("Invalid message")
