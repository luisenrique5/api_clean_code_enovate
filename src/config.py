import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

class Config:
    MONGO_URI = os.getenv('MONGO_URI')
    EXTERNAL_API = os.getenv('EXTERNAL_API')
    EXTERNAL_API_TOKEN = os.getenv('EXTERNAL_API_TOKEN')
    INTERNAL_API_TOKEN = os.getenv('INTERNAL_API_TOKEN')

    @staticmethod
    def get_mongo_collection(db_name='prodanalytics', collection_name='monthlyaverage'):
        client = MongoClient(Config.MONGO_URI)
        db = client[db_name]
        collection = db[collection_name]
        return collection
