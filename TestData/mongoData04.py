import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["runoobdb"]
mycol01 = mydb["sites"]
mycol02 = mydb["site2"]

result = mycol01.aggregate([
    {
        '$lookup':
            {
                "from": "site2",  # 需要联合查询的另一张表B
                "localField": "name",  # 表A的字段
                "foreignField": "name",  # 表B的字段
                "as": "name_docs"  # 根据A、B联合生成的新字段名
            },
    },
    {
        '$project':  # 联合查询后需要显示哪些字段，1：显示
            {
                'name': 1,
                'cn_name': 1,
                'address': 1,
                'task_docs.evidence_content': 1,
                'url': 1,
                'alexa': 1,
                '_id': 0,
            },
    },
    {
        '$match':  # 根据哪些条件进行查询
            {
                "name": 'RUNOOB'  # 这里是根据表A中 user_id == name
            }
    }
]
)

print('=====', result)
