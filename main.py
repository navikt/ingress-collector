import logging
import json_logging
import os
import sys
# noinspection PyPackageRequirements
from fastapi import FastAPI
from kubernetes import client, config, watch

# initiating logging
json_logging.ENABLE_JSON_LOGGING = True
json_logging.init_non_web()
logger = logging.getLogger()
logger.handlers = [logging.StreamHandler(sys.stdout)]
logging.getLogger('uvicorn.access').disabled = True


app = FastAPI()

try:
    config.load_kube_config()
except:
    config.load_incluster_config()

# if os.environ.get('NAIS_CLUSTER_NAME'):
#     logger.info("Loading incluster_config")
#     config.load_incluster_config()
# else:
#     config.load_kube_config()


test_watch = []


@app.on_event('startup')
async def fetch_namespaces():
    if os.getenv('KUBERNETES_SERVICE_HOST'):
        logger.info("KUBERNETES_SERVICE_HOST: " + os.getenv('KUBERNETES_SERVICE_HOST'))
    else:
        logger.warning("No KUBERNETES_SERVICE_HOST set in env.")
    v1 = client.CoreV1Api()
    # w = watch.Watch()
    # count = 10
    # for event in w.stream(v1.list_namespace, _request_timeout=60):
    #     test_watch.append(event)
    #     print("Event: %s %s" % (event['type'], event['object'].metadata.name))
    #     count -= 1
    #     if not count:
    #         w.stop()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/env")
async def root():
    return os.environ


@app.get("/test-watch")
async def root():
    return test_watch


@app.get('/is-alive')
async def is_healthy():
    return 'OK'


@app.get('/is-ready')
async def is_ready():
    return 'OK'
