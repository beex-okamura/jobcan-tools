from pydantic import BaseModel


class UserInfo(BaseModel):
    user_id: str
    jobcan_user_id: str
    jobcan_password: str
    slack_access_token: str
    send_punch_channel: list[str] | None
