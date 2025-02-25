import re

from slack_sdk import WebClient

from lib.secrets import get_secrets

clock_in_match = re.compile("^(出勤|:remote-syusya:|ws|syukin).*")
go_office_in_match = re.compile("^(出社|:butsurishussha:|syusya).*")
clock_out_match = re.compile("^(退勤|:remote-taisya:|wt|taisya).*")
go_out_match = re.compile("^(外出|:gaisyutsu:|go|gaisyutsu).*")
returned_match = re.compile("^(再入|:sainyu:|gr|sainyu).*")
leave_office_in_match = re.compile("^(退社|:butsuritaisya:|taisya).*")

work_message_attribute = {
    "clock_in": {
        "name": "出勤",
        "icon": ":remote-syusya:",
    },
    "go_office_in": {
        "name": "出社",
        "icon": ":butsurishussha:",
    },
    "clock_out": {
        "name": "退勤",
        "icon": ":remote-taisya:",
    },
    "go_out": {
        "name": "外出",
        "icon": ":gaisyutsu:",
    },
    "returned": {
        "name": "再入",
        "icon": ":sainyu:",
    },
    "leave_office_in_match": {
        "name": "退社",
        "icon": ":butsuritaisya:",
    },
}

secrets = get_secrets()


class Slack:
    def __init__(self, token: str | None = None) -> None:
        self.token = token
        self.slack = WebClient(
            token=token if token is not None else secrets.SLACK_BOT_USER_TOKEN
        )

    def send_message(self, channel: str, message: str):
        self.slack.chat_postMessage(channel=channel, text=message)

    def change_status(self, status_text: str, status_emoji: str):
        if self.token == secrets.SLACK_BOT_USER_TOKEN:
            raise ValueError("You can't change status of bot user")
        self.slack.users_profile_set(
            profile={"status_text": status_text, "status_emoji": status_emoji}
        )


def choice_work_message(message: str):
    if clock_in_match.match(message):
        return "clock_in"
    elif clock_out_match.match(message):
        return "clock_out"
    elif go_out_match.match(message):
        return "go_out"
    elif returned_match.match(message):
        return "returned"
    elif go_office_in_match.match(message):
        return "go_office_in"
    elif leave_office_in_match.match(message):
        return "leave_office_in"

    raise ValueError("Invalid message")
