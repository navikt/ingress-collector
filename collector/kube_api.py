from kubernetes import client, config, watch
from collector import nais

logger = nais.init_nais_logging()


def print_event_to_console(e):
    logger.warning("Event: %s %s (%s)" % (
        e['type'],
        e['object']['metadata']['name'],
        e['object']['metadata']['uid']))


def init_kube_client():
    try:
        config.load_kube_config()
    except:
        config.load_incluster_config()


def watch_nais_apps(callback_function):
    v1 = client.CustomObjectsApi()
    w = watch.Watch()
    for event in w.stream(v1.list_cluster_custom_object,
                          group="nais.io",
                          version="v1alpha1",
                          plural="applications"
                          ):
        if event["type"] != "ERROR":
            callback_function(event)
