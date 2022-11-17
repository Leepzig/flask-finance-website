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

def upload_csv(file_name):
    """ Imports a csv file at path csv_name to a mongo colection
    returns: count of the documants in the new collection
    """
    # data = pd.read_csv(f"/temp_test_csv/{file_name}")
    file_used = f"db/temp_test_csv/October_2022.csv"
    # payload = json.loads(data.to_json(orient='records'))
    # collumn.remove()
    # collection.insert_one(payload)

    with open(file_used, "rb") as f:
        encoded = Binary(f.read())
        collection.insert_one({"filename": file_used, "file": encoded, "description": "test" })



print(db["csvdocs"].count_documents({}))

upload_csv(file_name="October_2022.csv")

new_count = db["csvdocs"].count_documents({})
print(f"2nd Count: {new_count}")



# doc_count = collection.count_documents({})
# print(doc_count)