import logging
import os

log_level = os.getenv("LOG_LEVEL", "INFO")
logger = logging.getLogger("uvicorn.access")
logger.setLevel(log_level)
