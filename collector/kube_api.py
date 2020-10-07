from kubernetes.client import CustomObjectsApi
from kubernetes.watch import Watch
import kubernetes.config

from collector.nais import init_nais_logging

logger = init_nais_logging()


def init_kube_client():
    try:
        kubernetes.config.load_incluster_config()
    except:
        kubernetes.config.load_kube_config()


def watch_nais_apps(callback_function):

    try:
        kubernetes.config.load_incluster_config()
    except Exception as e:
        print(e)
        kubernetes.config.load_kube_config()

    v1 = CustomObjectsApi()

    data = v1.list_cluster_custom_object(group="nais.io",
                          version="v1alpha1",
                          plural="applications")

    print(data)

    w = Watch()

    logger.warning("    ")
    logger.warning("STARTING TO WATCH")
    logger.warning("    ")

    for event in w.stream(v1.list_cluster_custom_object,
                          group="nais.io",
                          version="v1alpha1",
                          plural="applications"):
        if event["type"] != "ERROR":
            callback_function(event)
