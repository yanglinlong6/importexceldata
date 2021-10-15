import json

import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["runoobdb"]
orderscol = mydb["orders"]

orderslist = [
    {"_id": 1, "item": "almonds", "price": 12, "quantity": 2},
    {"_id": 2, "item": "pecans", "price": 20, "quantity": 1},
    {"_id": 3}
]

orderscol.delete_many({})
x = orderscol.insert_many(orderslist)

inventorycol = mydb["inventory"]
inventorylist = [
    {"_id": 1, "sku": "almonds", "description": "product 1", "instock": 120},
    {"_id": 2, "sku": "bread", "description": "product 2", "instock": 80},
    {"_id": 3, "sku": "cashews", "description": "product 3", "instock": 60},
    {"_id": 4, "sku": "pecans", "description": "product 4", "instock": 70},
    {"_id": 5, "sku": None, "description": "Incomplete"},
    {"_id": 6}
]
inventorycol.delete_many({})
y = inventorycol.insert_many(inventorylist)

result = orderscol.aggregate([
    {
        '$lookup':
            {
                'from': "inventory",
                'localField': "item",
                'foreignField': "sku",
                'as': "inventory_docs"
            }
    },
    {
        '$project':
            {
                'sku': 1,
                'item': 1,
                'description': 1,
                'instock': 1,
                'price': 1,
                'quantity': 1
            }
    },
    {
        '$match':
            {
                "item": 'almonds'  # 这里是根据表A中 item == almonds
            }
    }
])

for document in result:
    print(document)
