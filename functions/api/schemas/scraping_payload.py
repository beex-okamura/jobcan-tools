from pydantic import BaseModel


class ScrapingPayload(BaseModel):
    channel: str
    user_id: str
    jobcan_user_id: str
    jobcan_password: str
