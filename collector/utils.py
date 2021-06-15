import sys
import logging
import json_logging


def init_app_logging():
    json_logging.init_non_web(enable_json=True)
    logging.getLogger('uvicorn.access').disabled = True


def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.handlers = [logging.StreamHandler(sys.stdout)]
    return logger
