import os
import threading
# noinspection PyPackageRequirements
from fastapi import FastAPI
from collector.kube_api import init_kube_client, watch_nais_apps, save_event_to_file
from collector.nais import init_nais_logging

# initiating logging
logger = init_nais_logging()
app = FastAPI()

test_watch = []


def watch_nais_callback(e):
    test_watch.append(e)
    save_event_to_file(e)


def watch_nais_task() -> None:
    watch_nais_apps(watch_nais_callback)


@app.on_event('startup')
async def application_startup():
    if os.getenv('KUBERNETES_SERVICE_HOST'):
        logger.info("KUBERNETES_SERVICE_HOST: " + os.getenv('KUBERNETES_SERVICE_HOST'))
    else:
        logger.warning("No KUBERNETES_SERVICE_HOST set in env.")

    # Loading kubernetes config
    init_kube_client()
    threading.Thread(target=watch_nais_task, daemon=True).start()


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
