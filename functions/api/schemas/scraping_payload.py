from pydantic import BaseModel


class ScrapingPayload(BaseModel):
    channel: str
    user_id: str
    jobcan_user_id: str
    jobcan_password: str
    zac_tenant_id: str
    zac_user_id: str
    zac_password: str
    choice_work_type: str
