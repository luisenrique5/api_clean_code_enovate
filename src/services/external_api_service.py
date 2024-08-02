import logging
import requests
from datetime import datetime
import os

logging.basicConfig(level=logging.INFO)

def fetch_and_process_data(mongo):
    url = os.getenv('EXTERNAL_API')
    token = os.getenv('EXTERNAL_API_TOKEN')
    headers = {
        'Authorization': f'Bearer {token}'
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status() 
        data = response.json()  # Convert the response to JSON
        logging.info("Data fetched from external API: %s", data)
        if data.get('apiStatus') and 'data' in data:
            process_data(data['data'], mongo)
        else:
            logging.error("Unexpected data structure: %s", data)
    except requests.exceptions.RequestException as e:
        logging.error("Error fetching data: %s", e)
    except ValueError as e:
        logging.error("Error parsing JSON: %s", e)

def process_data(data, mongo):
    if not isinstance(data, list):
        logging.error("Unexpected data format: %s", data)
        return

    collection = mongo.db.tracker_volume
    date_now = datetime.now().strftime("%Y-%m-%d")
    
    for entry in data:
        if not isinstance(entry, dict):
            logging.error("Unexpected entry format: %s", entry)
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

    doc["liquid_values"].append(liquid_value)
    doc["gas_values"].append(gas_value)

    doc["liquid_avg"] = sum(doc["liquid_values"]) / len(doc["liquid_values"])
    doc["gas_avg"] = sum(doc["gas_values"]) / len(doc["gas_values"])

    collection.update_one({"_id": doc["_id"]}, {"$set": doc})

def initialize_data(date, separator_type, liquid_value, gas_value, collection):
    doc = {
        "date": date,
        "separator_type": separator_type,
        "liquid_values": [liquid_value],
        "gas_values": [gas_value],
        "liquid_avg": liquid_value,
        "gas_avg": gas_value
    }
    result = collection.insert_one(doc)
