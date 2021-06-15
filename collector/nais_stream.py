import re

from typing import Callable

from kubernetes.client import ApiException

from collector.utils import get_logger

logger = get_logger(__name__)


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
        try:
            for event in self.w.stream(self.v1.list_cluster_custom_object,
                                       group="nais.io",
                                       version="v1alpha1",
                                       plural="applications",
                                       **kwargs):
                if event["type"] not in ["ERROR", "DELETED"]:
                    self.callback_function(event)
        except ApiException as api_exc:
            logger.warning(f"\n\nAPI exception: {api_exc.status}: Reason: {api_exc.reason}\n\n")
            if api_exc.status == 410:
                resource_version = api_exc.reason.split('(')
                raise TooOldResourceVersionError(resource_version[1][:-1])
            else:
                raise api_exc
