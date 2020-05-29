from kafka import KafkaProducer
from json import dumps

producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda x: dumps(x).encode('utf-8'),
    key_serializer=lambda x: str.encode(x)
)

for e in range(10):
    data = {'number': e}
    producer.send(
        key="key" + str(e),
        topic='my_favorite_topic',
        value=data)

producer.flush()
