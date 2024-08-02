import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    MONGO_URI = os.getenv('MONGO_URI')
    EXTERNAL_API = os.getenv('EXTERNAL_API')
    EXTERNAL_API_TOKEN = os.getenv('EXTERNAL_API_TOKEN')
    INTERNAL_API_TOKEN = os.getenv('INTERNAL_API_TOKEN')
