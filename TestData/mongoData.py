import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["runoobdb"]
dblist = myclient.list_database_names()
print(dblist)

# dblist = myclient.database_names()
if "runoobdb" in dblist:
    print("数据库已存在！")
else:
    print("数据库不存在!")

for dbname in dblist:
    print('dbname', dbname)
    # mydb = myclient["runoobdb"]
    mydb = myclient[dbname]
    for listname in mydb.list_collection_names():
        print('listname', listname)
        mycol = mydb[listname]
        for x in mycol.find():
            print(x)
