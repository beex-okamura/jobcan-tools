from pydantic import BaseModel


class AlexaUser(BaseModel):
    userId: str
    accessToken: str | None = None


class AlexaSession(BaseModel):
    user: AlexaUser


class AlexaIntent(BaseModel):
    name: str


class AlexaRequestBody(BaseModel):
    type: str
    intent: AlexaIntent | None = None


class AlexaRequest(BaseModel):
    version: str
    session: AlexaSession
    request: AlexaRequestBody
