from pydantic import BaseModel


class ShortcutPunchRequest(BaseModel):
    user_id: str
    work_type: str


class ShortcutPunchResponse(BaseModel):
    message: str
