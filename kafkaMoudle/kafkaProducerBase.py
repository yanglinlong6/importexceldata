import logging
import multiprocessing
import time
from kafka import KafkaProducer

log = logging.getLogger(__name__)


def worker(ch):
    producer = KafkaProducer(bootstrap_servers='192.168.3.182:9095', acks=0, retries=5)

    for i in range(1000):
        time.sleep(0.01)
        print('produce msg', i)
        producer.send('warn_topic', ch * 1024)

    producer.close()


if __name__ == '__main__':
    log.info("start===")
    p1 = multiprocessing.Process(target=worker, args=('1',))
    p2 = multiprocessing.Process(target=worker, args=('2',))
    p1.start()
    p2.start()
