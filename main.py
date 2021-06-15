import os
import threading
import prometheus_client as pc
# noinspection PyPackageRequirements
from fastapi import FastAPI
from starlette.responses import JSONResponse, Response
from starlette import status

from collector.metrics import STREAM_TIMEOUT_COUNTER
from collector.nais_stream import NaisStream, TooOldResourceVersionError
from collector.utils import init_app_logging, get_logger
from kubernetes import client, config, watch
from kafka_producer.kafka_producer import CollectorKafkaProducer

init_app_logging()
logger = get_logger(__name__)
app = FastAPI()
is_alive = True

producer = CollectorKafkaProducer()


def init_kube_client():
    try:
        config.load_incluster_config()
    except:
        config.load_kube_config()
    else:
        logger.info("loaded incluster config")


def app_watcher_callback(e):
    logger.info("Received event: %s %s (%s)" % (e['type'], e['object']['metadata']['name'], e['object']['metadata']['uid']))
    e.pop("type")
    e["cluster"] = os.environ["NAIS_CLUSTER_NAME"]
    e["application_type"] = "Nais_App"
    logger.info("Publishing " + e['object']['metadata']['name'] + " from cluster: " + e['cluster']
                + f" to topic {os.environ['KAFKA_TOPIC']}")
    producer.send(e)


def start_stream(stream, **kwargs):
    try:
        stream.watch(**kwargs)
    except TooOldResourceVersionError as resource_version_error:
        STREAM_TIMEOUT_COUNTER.inc()
        logger.warning(f"Retrying with resource version {resource_version_error.resource_version}")
        start_stream(stream, resource_version=resource_version_error.resource_version)


def app_watcher_task(callback_function) -> None:
    v1 = client.CustomObjectsApi()
    w = watch.Watch()

    stream = NaisStream(callback_function, v1, w)
    try:
        start_stream(stream)
    except:
        global is_alive
        is_alive = False
        raise


@app.on_event('startup')
def application_startup():
    logger.info('application_startup')
    if os.getenv('KUBERNETES_SERVICE_HOST'):
        logger.info("KUBERNETES_SERVICE_HOST: " + os.getenv('KUBERNETES_SERVICE_HOST'))
    else:
        logger.warning("No KUBERNETES_SERVICE_HOST set in env.")

    init_kube_client()
    threading.Thread(target=app_watcher_task, args=(app_watcher_callback,), daemon=True).start()


@app.get("/metrics")
def metrics():
    headers = {'Content-Type': pc.CONTENT_TYPE_LATEST}
    return Response(pc.generate_latest(pc.REGISTRY), status_code=status.HTTP_200_OK, headers=headers)


@app.get('/is-alive')
def is_healthy():
    if is_alive:
        return JSONResponse(status_code=status.HTTP_200_OK,
                            content={"Status": "OK"})
    else:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            content={"Error": "K8s stream stopped"})


@app.get('/is-ready')
def is_ready():
    return JSONResponse(status_code=status.HTTP_200_OK,
                        content={"Status": "OK"})
