import redis

# r = redis.StrictRedis(host="192.168.3.207", port=6379, db=0)
r = redis.StrictRedis(host="112.74.125.238", port=6379, db=0)
pipe = r.pipeline()

if __name__ == '__main__':
    pipe.set('yang', '1')
    pipe.set('lin', '2')
    pipe.set('long', '3')
    pipe.execute()
    # result = r.get('yang').decode('UTF-8')
    pipe.get('yang')
    pipe.get('lin')
    pipe.get('long')
    result = pipe.execute()
    print(result)
    for i in list(result):
        print(i.decode('UTF-8'))
