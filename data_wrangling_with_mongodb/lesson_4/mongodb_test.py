from pymongo import MongoClient
client = MongoClient('localhost:27017')
db = client.examples
print db.cities.find_one()
