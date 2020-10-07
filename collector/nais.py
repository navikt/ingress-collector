import logging
import json_logging
import sys


def init_nais_logging():
    json_logging.ENABLE_JSON_LOGGING = True
    json_logging.init_non_web()
    logger = logging.getLogger()
    logger.handlers = [logging.StreamHandler(sys.stdout)]
    logging.getLogger('uvicorn.access').disabled = True
    return logger
