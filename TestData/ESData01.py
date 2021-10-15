from elasticsearch import Elasticsearch

es = Elasticsearch(['127.0.0.1:9200'], ignore=[400, 405, 502])  # 以列表的形式忽略多个状态码  默认连接本地elasticsearch
print(es.info())
