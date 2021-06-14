import os
import json
from kafka import KafkaProducer
from kafka.errors import KafkaError


class IngressRetrieverKafkaProducer:

    def __init__(self):
        self.producer = KafkaProducer(bootstrap_servers=os.environ["KAFKA_BROKERS"],
                                      ssl_certfile=os.environ["KAFKA_CERTIFICATE_PATH"],
                                      ssl_keyfile=os.environ["KAFKA_PRIVATE_KEY_PATH"],
                                      ssl_cafile=os.environ["KAFKA_CA_PATH"],
                                      security_protocol='SSL')

    def send(self, event):
        try:
            future = self.producer.send(os.environ['KAFKA_TOPIC'], json.dumps(event).encode("utf-8"),
                                        key=bytes(event['object']['metadata']['uid'], encoding="utf-8"))
            result = future.get(timeout=60)
        except KafkaError:
            print("Reconnecting to kafka")
            self.producer = KafkaProducer(bootstrap_servers=os.environ["KAFKA_BROKERS"],
                                          ssl_certfile=os.environ["KAFKA_CERTIFICATE_PATH"],
                                          ssl_keyfile=os.environ["KAFKA_PRIVATE_KEY_PATH"],
                                          ssl_cafile=os.environ["KAFKA_CA_PATH"],
                                          security_protocol='SSL')
            future = self.producer.send(os.environ['KAFKA_TOPIC'], json.dumps(event).encode("utf-8"),
                                        key=bytes(event['object']['metadata']['uid'], encoding="utf-8"))
            result = future.get(timeout=60)

        print(result)
        print('App published: ' + event['object']['metadata']['name'] + ", cluster: " + event['cluster'] + ", UID: "
              + event['object']['metadata']['uid'])
        return result
