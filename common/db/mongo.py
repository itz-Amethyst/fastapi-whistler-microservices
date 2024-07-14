from pymongo import MongoClient


client = MongoClient("mongodb://mongodb:27017")
db = client['discounts_db'] 
discounts_collection = db['discounts']