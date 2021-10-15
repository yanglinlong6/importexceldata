import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["runoobdb"]
mycol = mydb["sites"]

myquery = {"alexa": "10000"}
newvalues = {"$set": {"alexa": "12345"}}

mycol.update_one(myquery, newvalues)

# 输出修改后的  "sites"  集合
for x in mycol.find():
    print(x)

print("=====")
myquery = {"name": {"$regex": "^F"}}
newvalues = {"$set": {"alexa": "123"}}
x = mycol.update_many(myquery, newvalues)
# 输出修改后的  "sites"  集合
for y in mycol.find():
    print(y)
print(x.modified_count, "文档已修改")

print("=====")
mydoc = mycol.find().sort("alexa")
for x in mydoc:
    print(x)

print("=====")
mydoc = mycol.find().sort("alexa", -1)
for x in mydoc:
    print(x)

print("=====")
myquery = {"name": "Taobao"}
mycol.delete_one(myquery)
# 删除后输出
for x in mycol.find():
    print(x)

# 删除集合中的所有文档
# x = mycol.delete_many({})
# print(x.deleted_count, "个文档已删除")

# 删除集合
# mycol.drop()
