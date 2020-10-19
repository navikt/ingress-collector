import re

from typing import Callable
from collector.nais import init_nais_logging

logger = init_nais_logging()


class TooOldResourceVersionError(Exception):

    def __init__(self, resource_version: str):
        self._resource_version = resource_version

    def __str__(self):
        return self._resource_version

    @property
    def resource_version(self):
        return self._resource_version

class NaisStream:

    def __init__(self, callback_function: Callable, v1, w):
        self.callback_function = callback_function
        self.v1 = v1
        self.w = w

    def watch(self, **kwargs):
        for event in self.w.stream(self.v1.list_cluster_custom_object,
                                   group="nais.io",
                                   version="v1alpha1",
                                   plural="applications",
                                   **kwargs):
            if event["type"] not in ["ERROR", "DELETED"]:
                self.callback_function(event)
            elif event["type"] == "ERROR" and event["object"]["code"] == 410:
                logger.warning("")
                logger.warning(event)
                logger.warning("")
                resource_version = event["object"]["message"].split('(')
                raise TooOldResourceVersionError(resource_version[1][:-1])
