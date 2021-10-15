from elasticsearch import Elasticsearch

es = Elasticsearch(['127.0.0.1:9200'], ignore=[400, 405, 502])  # 以列表的形式忽略多个状态码  默认连接本地elasticsearch
print(es.index(index='py2', doc_type='doc', id=1, body={'name': "张开", "age": 18}))
print(es.index(index='py2', doc_type='doc', id=1, body={'name': "张开2", "age": 18}))
print(es.index(index='py3', doc_type='doc', id=1, body={'name': "林龙", "age": 18}))
print(es.index(index='py3', doc_type='doc', id=2, body={'name': "杨林龙", "age": 18}))
print(es.index(index='py3', doc_type='doc', id=3, body={'name': "杨林", "age": 18}))
print(es.get(index='py2', doc_type='doc', id=1))
print(es.get(index='py3', doc_type='doc', id=2))

body = {
    "query": {
        "match_all": {}
    }
}

body01 = {
    "query": {
        "term": {
            "name": "龙"
        }
    }
}

body02 = {
    "query": {
        "terms": {
            "name": [
                "林", "android"
            ]
        }
    }
}

# query = es.search(index='py3', body=body)
# query = es.search(index='py3', body=body01)
query = es.search(index='py3', doc_type='doc', body=body02)
print(query)

query = es.search(index='py2', doc_type='doc')
print(query)
query = es.search(index='py3', doc_type='doc')
print(query)

# match:匹配name包含python关键字的数据
body03 = {
    "query": {
        "match": {
            "name": "杨"
        }
    }
}
query = es.search(index='py3', doc_type='doc', body=body03)
print(query)

print('multi_match')
body04 = {
    "query": {
        "multi_match": {
            "query": "18",
            "fields": ["name", "age"]
        }
    }
}
query = es.search(index='py3', doc_type='doc', body=body04)
print(query)

# 复合查询bool
# bool有3类查询关系，must(都满足),should(其中一个满足),must_not(都不满足)

body05 = {
    "query": {
        "bool": {
            "must": [
                {
                    "term": {
                        "name": "杨"
                    }
                },
                {
                    "term": {
                        "age": 18
                    }
                }
            ]
        }
    }
}

query = es.search(index='py3', doc_type='doc', body=body05)
print(query)

# 范围查询
body06 = {
    "query": {
        "range": {
            "age": {
                "gte": 18,  # >=18
                "lte": 30  # <=30
            }
        }
    }
}

query = es.search(index='py3', doc_type='doc', body=body06)
print(query)

body07 = {
    "query": {
        "prefix": {
            "name": "杨"
        }
    }
}

query = es.search(index='py3', doc_type='doc', body=body07)
print(query)

# 通配符查询
body08 = {
    "query": {
        "wildcard": {
            "name": "*杨*"
        }
    }
}

query = es.search(index='py3', doc_type='doc', body=body08)
print(query)

body09 = {
    "query": {
        "match_all": {}
    },
    "sort": {
        "age": {  # 根据age字段升序排序
            "order": "asc"  # asc升序，desc降序
        }
    }
}
query = es.search(index='py3', doc_type='doc', body=body09)
print(query)

print('获取最小值')
body10 = {
    "query": {
        "match_all": {}
    },
    "aggs": {  # 聚合查询
        "min_age": {  # 最小值的key
            "min": {  # 最小
                "field": "age"  # 查询"age"的最小值
            }
        }
    }
}
query = es.search(index='py3', doc_type='doc', body=body10)
print(query)

print('获取最大值')
body11 = {
    "query": {
        "match_all": {}
    },
    "aggs": {  # 聚合查询
        "max_age": {  # 最大值的key
            "max": {  # 最大
                "field": "age"  # 查询"age"的最大值
            }
        }
    }
}
query = es.search(index='py3', doc_type='doc', body=body11)
print(query)

print('获取和')
body12 = {
    "query": {
        "match_all": {}
    },
    "aggs": {  # 聚合查询
        "sum_age": {  # 和的key
            "sum": {  # 和
                "field": "age"  # 获取所有age的和
            }
        }
    }
}
query = es.search(index='py3', doc_type='doc', body=body12)
print(query)

print('获取平均值')
body13 = {
    "query": {
        "match_all": {}
    },
    "aggs": {  # 聚合查询
        "avg_age": {  # 平均值的key
            "sum": {  # 平均值
                "field": "age"  # 获取所有age的平均值
            }
        }
    }
}
query = es.search(index='py3', doc_type='doc', body=body13)
print(query)
