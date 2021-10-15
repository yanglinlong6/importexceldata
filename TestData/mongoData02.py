import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["runoobdb"]
mycol = mydb["sites"]

x = mycol.find_one()

print(x)

for x in mycol.find():
    print(x)

print("=====")

for x in mycol.find({}, {"_id": 0, "name": 1, "alexa": 1}):
    print(x)

print("=====")
for x in mycol.find({}, {"alexa": 0}):
    print(x)

print("=====")
myquery = {"name": "RUNOOB"}
mydoc = mycol.find(myquery, {"name": 1, "alexa": 1})
for x in mydoc:
    print(x)

print("=====")
myquery = {"name": {"$gt": "H"}}
mydoc = mycol.find(myquery)
for x in mydoc:
    print(x)

print("=====")
myquery = {"name": {"$regex": "^R"}}
mydoc = mycol.find(myquery)
for x in mydoc:
    print(x)

print("=====")
myresult = mycol.find().limit(3)
for x in myresult:
    print(x)
