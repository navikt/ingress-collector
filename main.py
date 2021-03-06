import os
import threading
import requests
import json
import backoff
# noinspection PyPackageRequirements
from fastapi import FastAPI
from starlette.responses import JSONResponse
from starlette import status
from collector.nais import init_nais_logging
from collector.kube_api import watch_nais_apps
from kubernetes import client, config

# initiating logging
logger = init_nais_logging()
app = FastAPI()
is_alive = True


@backoff.on_exception(backoff.expo, requests.exceptions.RequestException, max_tries=10)
def request_put(url, message):
    res = requests.put(url, json.dumps(message).encode("utf-8"))
    res.raise_for_status()
    logger.info(res)


def watch_nais_callback(e):
    logger.info("Event: %s %s (%s)" % (e['type'], e['object']['metadata']['name'], e['object']['metadata']['uid']))
    e.pop("type")
    e["cluster"] = os.environ["NAIS_CLUSTER_NAME"]
    e["application_type"] = "Nais_App"
    logger.info("Posting " + e['object']['metadata']['name'] + " to ingress-retriever prod")
    request_put(os.environ["RETRIEVER_URL_PROD"], e)

    if "RETRIEVER_URL_DEV" in os.environ:
        logger.info("Posting " + e['object']['metadata']['name'] + " to ingress-retriever dev")
        request_put(os.environ["RETRIEVER_URL_DEV"], e)


def init_kube_client():
    try:
        config.load_incluster_config()
    except:
        config.load_kube_config()
    else:
        logger.warning("loaded incluster config")


def watch_nais_task() -> None:
    try:
        watch_nais_apps(watch_nais_callback)
    except:
        global is_alive
        is_alive = False


@app.on_event('startup')
def application_startup():
    logger.info('application_startup')
    if os.getenv('KUBERNETES_SERVICE_HOST'):
        logger.info("KUBERNETES_SERVICE_HOST: " + os.getenv('KUBERNETES_SERVICE_HOST'))
    else:
        logger.warning("No KUBERNETES_SERVICE_HOST set in env.")

    # Loading kubernetes config
    init_kube_client()
    v1 = client.CustomObjectsApi()
    v1.list_cluster_custom_object(group="nais.io",
                                  version="v1alpha1",
                                  plural="applications")

    threading.Thread(target=watch_nais_task, daemon=True).start()


@app.get("/")
def root():
    return {"message": "Hello World"}


@app.get('/is-alive')
def is_healthy():
    if is_alive:
        return 'OK'
    else:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            content={"Error": "K8s stream stopped"})


@app.get('/is-ready')
def is_ready():
    return 'OK'
