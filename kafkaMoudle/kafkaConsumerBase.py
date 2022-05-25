from pykafka import KafkaClient


class KafkaTest(object):
    def __init__(self, host):
        self.host = host
        self.client = KafkaClient(hosts=self.host)
        print(self.client.topics)  # 所有的topic
        print(self.client.brokers)  # kafka的所有的brokers

    def balance_consumer(self, topic, offset=0):
        """
        使用balance consumer去消费kafka
        :return:
        """

        topic = self.client.topics[topic.encode()]
        # managed=True 设置后，使用新式reblance分区方法，不需要使用zk，而False是通过zk来实现reblance的需要使用zk,必须指定 # zookeeper_connect = "zookeeperIp",consumer_group='test_group',
        consumer = topic.get_balanced_consumer(
            auto_commit_enable=True,
            managed=True,
            # managed=False,
            # zookeeper_connect="10.111.64.225:2181",
            consumer_group=b'HpDailyDataConsumerGroup',
            consumer_timeout_ms=300000
        )

        partitions = topic.partitions
        print("所有的分区：{}".format(partitions))
        earliest_offsets = topic.earliest_available_offsets()
        print("最早可用offset：{}".format(earliest_offsets))
        last_offsets = topic.latest_available_offsets()
        print("最近可用offset：{}".format(last_offsets))
        offset = consumer.held_offsets
        print("当前消费者分区offset情况：{}".format(offset))
        while True:
            msg = consumer.consume()
            if msg:
                offset = consumer.held_offsets
                print("当前位移：{}".format(offset))
                # result.append(eval(msg.value.decode()))
                print(msg.value.decode())
                consumer.commit_offsets()  # commit一下

            else:
                print("没有数据")


if __name__ == '__main__':
    host = '192.168.3.182:9095'
    # host = 'c6140sv02:6667'
    kafka_ins = KafkaTest(host)
    topic = 'warn_topic'
    # topic = 'topic_jsonctr_collector_ws_data_daily'
    kafka_ins.balance_consumer(topic)
