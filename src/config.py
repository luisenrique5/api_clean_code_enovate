import os
from dotenv import load_dotenv
from pymongo import MongoClient
import json
from os.path import join, dirname

dotenv_path = join(dirname(__file__), '../env/.env')
load_dotenv(dotenv_path)

config_json_path = join(dirname(__file__), '../config/config.json')
with open(config_json_path, 'r') as f:
    config_data = json.load(f)

class Config:
    MONGO_URI = os.getenv('MONGO_URI')
    EXTERNAL_API = os.getenv('EXTERNAL_API')
    EXTERNAL_API_TOKEN = os.getenv('EXTERNAL_API_TOKEN')
    INTERNAL_API_TOKEN = os.getenv('INTERNAL_API_TOKEN')
    ENVIRONMENT = config_data["ENVIRONMENT"]
    LOGGINGLEVEL = config_data["LOGGINGLEVEL"]
    REMOTEDOCKERIMAGE = config_data["REMOTEDOCKERIMAGE"]
    KEYPATH = config_data["KEYPATH"]

    @staticmethod
    def get_mongo_collection(db_name='prodanalytics', collection_name='monthlyaverage'):
        client = MongoClient(Config.MONGO_URI)
        db = client[db_name]
        collection = db[collection_name]
        return collection
