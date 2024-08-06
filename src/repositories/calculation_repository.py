from datetime import datetime
from src.config import Config

def get_monthly_data(mongo, separator_type, year, month): 
    collection = Config.get_mongo_collection()
    db_results = collection.find({
        "separator_type": separator_type,
        "date": {
            "$gte": f"{year}-{month:02d}-01",
            "$lte": f"{year}-{month:02d}-{datetime.now().day:02d}"
        }
    })
    return db_results
