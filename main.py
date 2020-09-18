import os
import threading
# noinspection PyPackageRequirements
from fastapi import FastAPI
from collector import kube_api, nais, kafka_producer

# initiating logging
logger = nais.init_nais_logging()
app = FastAPI()


def watch_nais_callback(e):
    kube_api.print_event_to_console(e)
    kafka_producer.produce_message(e)


def watch_nais_task() -> None:
    kube_api.watch_nais_apps(watch_nais_callback)


@app.on_event('startup')
def application_startup():
    logger.info('application_startup')
    if os.getenv('KUBERNETES_SERVICE_HOST'):
        logger.info("KUBERNETES_SERVICE_HOST: " + os.getenv('KUBERNETES_SERVICE_HOST'))
    else:
        logger.warning("No KUBERNETES_SERVICE_HOST set in env.")

    # Loading kubernetes config
    kube_api.init_kube_client()
    threading.Thread(target=watch_nais_task, daemon=True).start()


@app.get("/")
def root():
    return {"message": "Hello World"}


@app.get('/is-alive')
def is_healthy():
    return 'OK'


@app.get('/is-ready')
def is_ready():
    return 'OK'
