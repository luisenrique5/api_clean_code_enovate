from .services import VolumeTracker, fetch_and_process_data_service

def fetch_and_process_data(api_url, headers):
    liquid_tracker = VolumeTracker("liquid")
    gas_tracker = VolumeTracker("gas")
    fetch_and_process_data_service(api_url, headers, liquid_tracker, gas_tracker)
    return {
        "liquid_monthly_average": liquid_tracker.get_monthly_average(),
        "gas_monthly_average": gas_tracker.get_monthly_average()
    }
