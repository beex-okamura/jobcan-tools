from enum import Enum
from pydantic import BaseModel

class ActionTypeEnum(str, Enum):
    url_verification = 'url_verification'
    rich_text_section = 'rich_text_section'
    message = 'message'
    event_callback = 'event_callback'


class ActionEventTypeEnum(str, Enum):
    message = 'message'


class SlackActionEvent(BaseModel):
    client_msg_id: str | None = None
    type: ActionEventTypeEnum
    user: str
    text: str
    ts: str
    blocks: list[dict] | None = None
    elements: list[dict] | None = None
    team: str
    channel: str
    event_ts: str
    channel_type: str


class SlackActionRequest(BaseModel):
    token: str
    bot_id: str | None = None
    team_id: str | None = None
    api_app_id: str | None = None
    challenge: str | None = None
    type: ActionTypeEnum
    event: SlackActionEvent | None = None
    authed_teams: list[str] | None = None
    event_id: str | None = None
    event_time: float | None = None


class SlackSendMessageRequest(BaseModel):
    token: str
    channel: str
    text: str

class SlackActionResponse(BaseModel):
    challenge: str | None
