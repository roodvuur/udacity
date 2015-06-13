import json

def insert_data(data, db):
    collection = db.arachnid
    # Your code here. Insert the data into a collection 'arachnid'
    collection.insert(data)


if __name__ == "__main__":
    
    from pymongo import MongoClient
    client = MongoClient("mongodb://localhost:27017")
    db = client.examples

    with open('arachnid.json') as f:
        data = json.loads(f.read())
        insert_data(data, db)
        print db.arachnid.find_one()