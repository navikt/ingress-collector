import logging
import json_logging
import sys
import os


def init_nais_logging():
    json_logging.ENABLE_JSON_LOGGING = True
    json_logging.init_non_web()
    logger = logging.getLogger()
    logger.handlers = [logging.StreamHandler(sys.stdout)]
    logging.getLogger('uvicorn.access').disabled = True
    return logger


def remove_no_proxy_domain(domain, envvarname):
    no_proxy = os.environ.get(envvarname, '')
    list_of_domains = no_proxy.split(",")
    if domain in list_of_domains:
        list_of_domains.remove(domain)
        domains = ",".join(list_of_domains)
        os.environ[envvarname] = domains

