from kafka import KafkaConsumer

consumer = KafkaConsumer(
    'my_favorite_topic',
    bootstrap_servers='localhost:9092'
)
for msg in consumer:
    print(msg)
