from pymongo import MongoClient


client = MongoClient("mongodb+srv://leepzig:1234@finance-app-db.m5ozabc.mongodb.net/?retryWrites=true&w=majority")
db = client.test

db = client['testDB']
# collection = db['testCol']
# db.create_collection("csvdocs", { "capped":True, "autoIndexID":True, "size" : 6142800, "max" : 10000}) 

db['csvdocs'].insert_one({"name":"Andrew","age":31})

print(db["csvdocs"].count_documents({}))




# doc_count = collection.count_documents({})
# print(doc_count)