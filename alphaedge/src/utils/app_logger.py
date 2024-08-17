import logging
from fastapi.logger import logger as fastapi_logger
from loguru import logger
import sys

# Remove the default logger to avoid duplicate logs
logger.remove()

# Add a new logger with a custom format
logger.add(sys.stdout, format="{time} - {level} - {message}", level="INFO")

# InterceptHandler class to redirect logs to Loguru


class InterceptHandler(logging.Handler):
    def emit(self, record):
        loguru_logger_opt = logger.opt(depth=6, exception=record.exc_info)
        loguru_logger_opt.log(record.levelno, record.getMessage())


# Set up basic logging configuration with the intercept handler
logging.basicConfig(handlers=[InterceptHandler()], level=0)

# Assign the intercept handler to Uvicorn and FastAPI loggers
uvicorn_loggers = [
    "uvicorn",
    "uvicorn.error",
    "uvicorn.access",
    "uvicorn.asgi",
    "uvicorn.lifespan",
    "uvicorn.server",
]

for uvicorn_logger in uvicorn_loggers:
    uvicorn_logger_instance = logging.getLogger(uvicorn_logger)
    uvicorn_logger_instance.handlers = [InterceptHandler()]
    uvicorn_logger_instance.propagate = False
    # Suppress INFO and lower logs
    uvicorn_logger_instance.setLevel(logging.WARNING)

# Suppress FastAPI's default logs
fastapi_logger.handlers = [InterceptHandler()]
fastapi_logger.setLevel(logging.WARNING)  # Suppress INFO and lower logs