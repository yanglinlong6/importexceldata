import redis

pool = redis.ConnectionPool(host='127.0.0.1', port=6379, decode_responses=True)
r = redis.Redis(connection_pool=pool)

r.set('name', 'zhangsan')

print(r.get('name'))

# 批量设置值
# r.mset(name1='zhangsan', name2='lisi')
# 或
print(r.mget({"name1": 'zhangsan', "name2": 'lisi'}))

# 批量获取
print(r.mget("name1", "name2"))
# 或
li = ["name1", "name2"]

print(r.mget(li))

r.set("cn_name", "君惜大大")  # 汉字
print(r.getrange("cn_name", 0, 2))  # 取索引号是0-2 前3位的字节 君 切片操作 （一个汉字3个字节 1个字母一个字节 每个字节8bit）
print(r.getrange("cn_name", 0, -1))  # 取所有的字节 君惜大大 切片操作
r.set("en_name", "junxi")  # 字母
print(r.getrange("en_name", 0, 2))  # 取索引号是0-2 前3位的字节 jun 切片操作 （一个汉字3个字节 1个字母一个字节 每个字节8bit）
print(r.getrange("en_name", 0, -1))  # 取所有的字节 junxi 切片操作

r.setrange("en_name", 1, "ccc")
print(r.get("en_name"))  # jccci 原始值是junxi 从索引号是1开始替换成ccc 变成 jccci

r.hset("hash1", "k1", "v1")
r.hset("hash1", "k2", "v2")
print(r.hkeys("hash1"))  # 取hash中所有的key
print(r.hget("hash1", "k1"))  # 单个取hash的key对应的值
print(r.hmget("hash1", "k1", "k2"))  # 多个取hash的key对应的值
r.hsetnx("hash1", "k2", "v3")  # 只能新建
print(r.hget("hash1", "k2"))

r.hmset("hash2", {"k2": "v2", "k3": "v3"})

print(r.hget("hash2", "k2"))  # 单个取出"hash2"的key-k2对应的value
print(r.hmget("hash2", "k2", "k3"))  # 批量取出"hash2"的key-k2 k3对应的value --方式1
print(r.hmget("hash2", ["k2", "k3"]))  # 批量取出"hash2"的key-k2 k3对应的value --方式2

print(r.hgetall("hash1"))
r.hdel("hash1", "k2")  # 删除一个键值对

r.lpush("list1", 11, 22, 33)
print(r.lrange('list1', 0, -1))
# 保存顺序为: 33,22,11
#
# 扩展：

r.rpush("list2", 11, 22, 33)  # 表示从右向左操作
print(r.llen("list2"))  # 列表长度
print(r.lrange("list2", 0, 3))  # 切片取出值，范围是索引号0-3
