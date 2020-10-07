from kubernetes.client import CustomObjectsApi
from kubernetes.watch import Watch
from kubernetes.config import load_kube_config, load_incluster_config


def init_kube_client():
    try:
        load_incluster_config()
    except:
        load_kube_config()


def watch_nais_apps(callback_function):

    try:
        load_incluster_config()
    except Exception as e:
        logger.warning(e)
        load_kube_config()

    v1 = CustomObjectsApi()
    w = Watch()
    for event in w.stream(v1.list_cluster_custom_object,
                          group="nais.io",
                          version="v1alpha1",
                          plural="applications"
                          ):
        if event["type"] != "ERROR":
            callback_function(event)
