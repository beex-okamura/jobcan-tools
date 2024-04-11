from pydantic import BaseModel


class UserInfo(BaseModel):
    user_id: str
    jobcan_user_id: str
    jobcan_password: str
