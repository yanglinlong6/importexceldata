import redis

r = redis.StrictRedis(host="192.168.3.207", port=6379, db=0)
pipe = r.pipeline()
# snList = []

if __name__ == '__main__':
    # for sn in snList:
    # pipe.delete("biz_gpsbs_".join(sn).join("_GPS"))
    # pipe.delete("biz_gpsbs_".join(sn).join("_BS"))
    # pipe.delete("biz_gpsbs_".join(sn).join("_StayStatus"))
    # keys = pipe.keys("")
    # print(str(keys))
    # pipe.execute()
    print("0")
    r.set('foo', 'bar')
    result = r.get('foo').decode('UTF-8')
    result02 = pipe.get('foo')
    pipe.execute()
    print(result)
    print(result02)
