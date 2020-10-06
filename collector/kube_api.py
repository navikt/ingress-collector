from collector import nais

logger = nais.init_nais_logging()


def print_event_to_console(e):
    logger.warning("Event: %s %s (%s)" % (
        e['type'],
        e['object']['metadata']['name'],
        e['object']['metadata']['uid']))


def init_kube_client():
    from kubernetes import config
    try:
        config.load_incluster_config()
    except:
        config.load_kube_config()


def watch_nais_apps(callback_function):
    from kubernetes import client, watch, config

    try:
        config.load_incluster_config()
    except Exception as e:
        logger.warning("SE NED")
        logger.warning("")
        logger.warning(e)
        logger.warning("")
        config.load_kube_config()
        logger.warning("SE OPP")
    else:
        logger.warning("KORREKT")

    v1 = client.CustomObjectsApi()
    w = watch.Watch()
    for event in w.stream(v1.list_cluster_custom_object,
                          group="nais.io",
                          version="v1alpha1",
                          plural="applications"
                          ):
        if event["type"] != "ERROR":
            callback_function(event)
