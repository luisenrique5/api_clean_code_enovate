from flask import Blueprint, request, jsonify
from src.services.volume_tracker_service import fetch_and_process_data_service
from src.models.volume_tracker_model import VolumeTracker
from src.utils.error_handling import handle_errors

average_bp = Blueprint('average', __name__)

@average_bp.route('/fetch-data', methods=['POST'])
@handle_errors
def fetch_data():
    data = request.json
    api_url = data.get('api_url')
    headers = data.get('headers')
    
    if not api_url or not headers:
        return jsonify({"error": "api_url y headers son requeridos"}), 400

    liquid_tracker = VolumeTracker("liquid")
    gas_tracker = VolumeTracker("gas")

    fetch_and_process_data_service(api_url, headers, liquid_tracker, gas_tracker)
    
    return jsonify({
        "liquid_monthly_average": liquid_tracker.get_monthly_average(),
        "gas_monthly_average": gas_tracker.get_monthly_average()
    }), 200
