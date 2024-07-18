from fastapi.logger import logger as fastapi_logger
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

fastapi_logger.handlers = logger.handlers
fastapi_logger.setLevel(logger.level)
