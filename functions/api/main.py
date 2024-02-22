import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum

from lib.environment import get_environment
from routers.slack import router as slack_actions

env = get_environment()

app = (
    FastAPI()
    if env.stage == "prod"
    else FastAPI(
        redoc_url="/api/redoc",
        docs_url="/api/docs",
        openapi_url="/api/docs/openapi.json",
    )
)
allow_origins = ["*"]

# CORS: https://fastapi.tiangolo.com/tutorial/cors/
app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(slack_actions)

PROJECT_ROOT = os.path.realpath(
    os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
)

handler = Mangum(app)
