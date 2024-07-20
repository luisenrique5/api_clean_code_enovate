import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    API_URL_BASE = os.getenv('API_URL_BASE')
    API_TOKEN = os.getenv('API_TOKEN')
