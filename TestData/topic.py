import pykafka as pykafka

client = pykafka.KafkaClient(hosts="127.0.0.1:9092")

print(client.topics)
