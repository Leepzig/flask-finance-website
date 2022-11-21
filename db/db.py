from pymongo import MongoClient
import base64
import bson
from bson.binary import Binary

client = MongoClient("mongodb+srv://leepzig:1234@finance-app-db.m5ozabc.mongodb.net/?retryWrites=true&w=majority")
db = client["finance-app-db"]
collection = db["csvdocs"]


# collection = db['testCol']
# db.create_collection("csvdocs", { "capped":True, "autoIndexID":True, "size" : 6142800, "max" : 10000}) 

# db['csvdocs'].insert_one({"name":"Andrew","age":31})

def upload_csv(file_path):
    """ Imports a csv file at path csv_name to a mongo collection
    returns: count of the documants in the new collection
    """
    file_name = file_path.split("/")[-1]

    with open(file_path, "rb") as f:
        encoded = Binary(f.read())
        collection.insert_one({"filename": file_name, "file": encoded, "description": "test" })


def get_csv():
    return collection.find_one({"filename":"October_2022.csv"})



print(db["csvdocs"].count_documents({"description":"test"}))

# upload_csv(file_path=f"db/temp_test_csv/October_2022.csv")
print(get_csv())
# db["csvdocs"].delete_many({"description":"test"})
new_count = db["csvdocs"].count_documents({})
print(f"2nd Count: {new_count}")



# doc_count = collection.count_documents({})
# print(doc_count)