from prometheus_client import Counter, Summary

# Node by id
STREAM_TIMEOUT_COUNTER = Counter('ingress_collector_counter_k8s_stream_timeout',
                                 'Counter value for number of k8s watch timeouts')
