from flask import Blueprint, request, jsonify
from src.services.volume_tracker_service import fetch_and_process_data_service
from src.utils.error_handling import handle_errors
from src.config import Config
from src.models.volume_tracker_model import VolumeTracker

main_bp = Blueprint('main', __name__)

@main_bp.route('/fetch_data/<country>/<region>/<well>/<well_number>', methods=['GET'])
@handle_errors
def fetch_data(country, region, well, well_number):
    """
    Endpoint para obtener y procesar datos de volúmenes basado en parámetros de ruta.
    """
    try:
        # Validar si el header de autorización está presente
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify({"error": "Authorization header is required"}), 400

        api_url = f"{Config.API_URL_BASE}/{country}/{region}/{well}/{well_number}"
        headers = {
            "Authorization": auth_header
        }

        liquid_tracker = VolumeTracker("liquid")
        gas_tracker = VolumeTracker("gas")

        result = fetch_and_process_data_service(api_url, headers, liquid_tracker, gas_tracker)

        return jsonify(result), 200
    except RuntimeError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "An unexpected error occurred"}), 500
