import json
import traceback

from kafka import KafkaProducer
from kafka.errors import kafka_errors


def producer_demo():
    # 假设生产的消息为键值对（不是一定要键值对），且序列化方式为json
    producer = KafkaProducer(
        bootstrap_servers=['localhost:9092'],
        key_serializer=lambda k: json.dumps(k).encode(),
        value_serializer=lambda v: json.dumps(v).encode())

    # 发送三条消息
    for i in range(0, 6):
        future = producer.send(
            'kafka_demo',
            key='count_num',  # 同一个key值，会被送至同一个分区
            value=str(i),
            partition=None
        )  # 向分区1发送消息
        print("send {}".format(str(i)))
        try:
            future.get(timeout=10)  # 监控是否发送成功
        except kafka_errors:  # 发送失败抛出kafka_errors
            traceback.format_exc()


if __name__ == '__main__':
    producer_demo()
