from kubernetes import client, config, watch
from pprint import pprint
import json

try:
    config.load_kube_config()
except:
    config.load_incluster_config()

v1 = client.CustomObjectsApi()
conf = client.Configuration()
pprint(vars(client.Configuration()))

w = watch.Watch()
data = {}
for event in w.stream(v1.list_cluster_custom_object,
                      group="nais.io",
                      version="v1alpha1",
                      plural="applications"
                      ):
    data = event
    print("Event: %s %s (%s)" % (
        event['type'],
        event['object']['metadata']['name'],
        event['object']['metadata']['uid'])
          )

with open('test.json', 'w') as outfile:
    json.dump(data, outfile, default=str)
