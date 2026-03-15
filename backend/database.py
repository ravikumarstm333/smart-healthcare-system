from pymongo import MongoClient
from config.settings import MONGO_URL, DATABASE_NAME

client = MongoClient(MONGO_URL)

db = client[DATABASE_NAME]

prediction_collection = db["predictions"]
users_collection = db["users"]
appointments_collection = db["appointments"]