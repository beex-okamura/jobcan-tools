import logging
import os
from fastapi import Request, Response
from fastapi.concurrency import iterate_in_threadpool
from starlette.middleware.base import BaseHTTPMiddleware

log_level = os.getenv('LOG_LEVEL', 'INFO')
logger = logging.getLogger('uvicorn.access')
logger.setLevel(log_level)


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        logger.info(f'Request: {request.method} {request.url.path} {request.url.query}')

        response: Response = await call_next(request)

        logger.info(f'Response: {response.status_code}')  # type: ignore
        logger.info(f'Response header: {response.headers}')
        response_body = [chunk async for chunk in response.body_iterator]
        response.body_iterator = iterate_in_threadpool(iter(response_body))
        logger.info(f"response_body={response_body[0].decode()}")

        return response
