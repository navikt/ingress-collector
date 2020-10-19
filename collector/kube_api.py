from kubernetes import client, watch
from collector.nais import init_nais_logging
from collector.nais_stream import NaisStream, TooOldResourceVersionError


logger = init_nais_logging()


def watch_nais_apps(callback_function):
    v1 = client.CustomObjectsApi()
    w = watch.Watch()

    stream = NaisStream(callback_function, v1, w)

    try:
        stream.watch()
    except TooOldResourceVersionError as resource_version:
        stream.watch(resource_version=resource_version)
