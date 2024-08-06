import requests
from datetime import datetime
import os
from src.config import Config

def fetch_and_process_data():
    url = os.getenv('EXTERNAL_API')
    token = os.getenv('EXTERNAL_API_TOKEN')
    headers = {
        'Authorization': f'Bearer {token}'
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status() 
        data = response.json()  
        if data.get('apiStatus') and 'data' in data:
            process_data(data['data'])
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
    except ValueError as e:
        print(f"Error parsing JSON: {e}")

def process_data(data):
    if not isinstance(data, list):
        print(f"Unexpected data format: {data}")
        return

    collection = Config.get_mongo_collection()
    date_now = datetime.now().strftime("%Y-%m-%d")
    
    for entry in data:
        if not isinstance(entry, dict):
            print(f"Unexpected entry format: {entry}")
            continue

        lsd = entry.get("LSD")
        if "IP Separator" in lsd or "LP Separator" in lsd:
            separator_type = "IP Separator" if "IP Separator" in lsd else "LP Separator"
            current_date = datetime.now().day

            if current_date == 1:
                liquid_value = entry.get("Liquid Flow Rate")
                gas_value = entry.get("Corrected Current Day Volume")
            else:
                liquid_value = entry.get("Liquid Previous Day Total")
                gas_value = entry.get("Corrected Previous Day Volume")

            if liquid_value != -999.25 and gas_value != -999.25:
                doc = collection.find_one({"date": date_now, "separator_type": separator_type})
                
                if doc:
                    update_data(doc, liquid_value, gas_value, collection)
                else:
                    initialize_data(date_now, separator_type, liquid_value, gas_value, collection)

def update_data(doc, liquid_value, gas_value, collection):
    count = doc.get("count", 0) + 1

    doc["liquid_avg"] = ((doc.get("liquid_avg", 0) * (count - 1)) + liquid_value) / count
    doc["gas_avg"] = ((doc.get("gas_avg", 0) * (count - 1)) + gas_value) / count
    doc["count"] = count

    collection.update_one({"_id": doc["_id"]}, {"$set": doc})

def initialize_data(date, separator_type, liquid_value, gas_value, collection):
    doc = {
        "date": date,
        "separator_type": separator_type,
        "liquid_avg": liquid_value,
        "gas_avg": gas_value,
        "count": 1
    }
    result = collection.insert_one(doc)
