from kafka import KafkaProducer
import os
import json

producer = KafkaProducer(bootstrap_servers=os.environ["KAFKA_BROKERS"],
                         ssl_certfile=os.environ["KAFKA_CERTIFICATE_PATH"],
                         ssl_keyfile=os.environ["KAFKA_PRIVATE_KEY_PATH"],
                         ssl_cafile=os.environ["KAFKA_CA_PATH"],
                         security_protocol='SSL')


def produce_message(message: dict):
    message.pop("type")
    message["cluster"] = os.environ["NAIS_CLUSTER_NAME"]
    future = producer.send('dataplattform.ingress-topic', json.dumps(message).encode("utf-8"),
                           key=bytes(message['metadata']['uid'], encoding="utf-8"))
    result = future.get(timeout=60)
    print(result)
