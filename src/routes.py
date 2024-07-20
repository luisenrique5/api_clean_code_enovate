from flask import Blueprint, request, jsonify
from .main.controllers import fetch_and_process_data

main_bp = Blueprint('main', __name__)

@main_bp.route('/fetch_data/<country>/<region>/<well>/<well_number>', methods=['GET'])
def fetch_data(country, region, well, well_number):
    try:
        api_url = f"https://apigateway1.enovate.app/prodanalytics-inputdata-test/iotwelldata/w&toffshore/{country}/{region}/{well}/{well_number}"
        headers = {
            "Authorization": "Token SMFGAHDJVqUr2xWifzjpLWC66qdNCPjFGonBROOKs"
        }

        result = fetch_and_process_data(api_url, headers)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 400
