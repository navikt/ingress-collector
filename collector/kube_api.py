from kubernetes import client, watch
from collector.nais import init_nais_logging


logger = init_nais_logging()


def watch_nais_apps(callback_function):
    v1 = client.CustomObjectsApi()
    w = watch.Watch()

    logger.warning("    ")
    logger.warning("STARTING TO WATCH")
    logger.warning("    ")

    for event in w.stream(v1.list_cluster_custom_object,
                          group="nais.io",
                          version="v1alpha1",
                          plural="applications"):
        if event["type"] != "ERROR":
            callback_function(event)
