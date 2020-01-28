from json import load
from pymongo import MongoClient
client = MongoClient('mongodb://localhost:27017/')
db = client.data
lifetime = db.lifetime

with open('LifeTime.json') as file:
	f = load(file)
	lifetime.insert_many(f['DatasComposant'])