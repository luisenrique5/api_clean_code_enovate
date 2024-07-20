import requests
from src.models.volume_tracker_model import VolumeTracker

def fetch_and_process_data_service(api_url, headers, liquid_tracker, gas_tracker):
    try:
        response = requests.get(api_url, headers=headers, verify=False)
        response.raise_for_status()
        data = response.json().get('data', [])

        if not data:
            raise RuntimeError("No data returned from API")

        for entry in data:
            if "IP Separator" in entry["LSD"]:
                date_str = entry["Date (MM/DD/YYYY)"]
                liquid_daily_volume = entry["Liquid Flow Rate"]
                liquid_yday_volume = entry["Liquid Previous Day Total"]
                gas_daily_volume = entry["Corrected Current Day Volume"]
                gas_yday_volume = entry["Corrected Previous Day Volume"]

                liquid_tracker.process_data(date_str, liquid_daily_volume, liquid_yday_volume)
                gas_tracker.process_data(date_str, gas_daily_volume, gas_yday_volume)
        
        return {
            "liquid_monthly_average": liquid_tracker.get_monthly_average(),
            "gas_monthly_average": gas_tracker.get_monthly_average()
        }
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Error during the request: {e}")
    except KeyError as e:
        raise RuntimeError(f"Error processing data: {e}")
