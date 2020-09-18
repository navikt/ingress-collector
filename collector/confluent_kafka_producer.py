import json

from confluent_kafka import Producer
import os


def produce_callback(error, msg):
    if error is not None:
        print(f"Failed to produce kafka message to topic {msg.topic()}: {error}")
    else:
        print(f"Message produced successfully to topic {msg.topic()}")


config = {
    "bootstrap.servers": os.environ["KAFKA_BROKERS"],
    "ssl.ca.location": os.environ["KAFKA_CA_PATH"],
    "ssl.key.location": os.environ["KAFKA_PRIVATE_KEY_PATH"],
    "ssl.certificate.location": os.environ["KAFKA_CERTIFICATE_PATH"],
    "security.protocol": "SSL"
}

try:
    kafka_producer = Producer(config)
except:
    print("ERRORERRORERROR")


def produce_message(message):
    kafka_producer.produce('dataplattform.ingress-topic', json.dumps(message).encode('utf-8'),
                           callback=produce_callback)
    kafka_producer.flush()
