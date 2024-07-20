from flask import Blueprint, request, jsonify
from src.models.volume_tracker_model import VolumeTracker
from src.services.data_fetcher import fetch_and_process_data

bp = Blueprint('volume', __name__)

@bp.route('/track-volume', methods=['GET'])
def track_volume():
    api_url = request.args.get('api_url')
    liquid_tracker = VolumeTracker("liquido")
    gas_tracker = VolumeTracker("gas")

    headers = {
        "Authorization": "Token SMFGAHDJVqUr2xWifzjpLWC66qdNCPjFGonBROOKs"
    }

    fetch_and_process_data(api_url, headers, liquid_tracker, gas_tracker)

    return jsonify({
        "liquid_monthly_average": liquid_tracker.get_monthly_average(),
        "gas_monthly_average": gas_tracker.get_monthly_average()
    })
