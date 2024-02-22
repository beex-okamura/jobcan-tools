import time
from typing import Callable

from fastapi import Request, Response
from fastapi.routing import APIRoute

from lib.logger import logger


class TimedRoute(APIRoute):
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            before = time.time()
            logger.info(
                f"Request: {request.method} {request.url.path} {request.url.query}"
            )
            response: Response = await original_route_handler(request)
            duration = time.time() - before
            logger.info(f"Response: {response.status_code}")
            logger.info(f"Response header: {response.headers}")
            logger.info(f"Response duration: {duration}")

            if response.body:
                logger.info(response.body.decode("utf-8"))

            return response

        return custom_route_handler
