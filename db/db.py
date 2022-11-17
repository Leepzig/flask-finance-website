from pymongo import MongoClient
import bson
import json
import pandas as pd

client = MongoClient("mongodb+srv://leepzig:1234@finance-app-db.m5ozabc.mongodb.net/?retryWrites=true&w=majority")
db = client["csvdocs"]


# collection = db['testCol']
# db.create_collection("csvdocs", { "capped":True, "autoIndexID":True, "size" : 6142800, "max" : 10000}) 

# db['csvdocs'].insert_one({"name":"Andrew","age":31})

def upload_csv(file_name, collumn_name):
    """ Imports a csv file at path csv_name to a mongo colection
    returns: count of the documants in the new collection
    """
    db = client["csvdocs"]
    # data = pd.read_csv(f"/temp_test_csv/{file_name}")
    data = pd.read_csv(f"db/temp_test_csv/October_2022.csv")
    payload = json.loads(data.to_json(orient='records'))
    # collumn.remove()
    db["cvsdocs"].insert(payload)
    return db["cvsdocs"].count()


print(db["csvdocs"].count_documents({}))

upload_csv(file_name="October_2022.csv", collumn_name="csv" )

new_count = db["csvdocs"].count_documents({})
print(f"2nd Count: {new_count}")



# doc_count = collection.count_documents({})
# print(doc_count)