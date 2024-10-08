from flask import request, jsonify
from src.auth import token_required
from src.services.calculation_service import perform_calculations

stored_results = {}

def register_calculation_routes(bp, mongo):
    @bp.route('/calculate_averages_volume', methods=['POST'])
    @token_required
    def calculate():
        global stored_results
        data = request.json
        if not data or 'wells' not in data:
            return jsonify({"message": "Invalid request, 'wells' data is missing"}), 400

        try:
            stored_results = perform_calculations(data, mongo)  # Aquí está el segundo argumento
            return jsonify({"message": "Data received successfully"}), 200
        except Exception as e:
            return jsonify({"message": "An error occurred during calculations", "error": str(e)}), 500

    @bp.route('/results_averages_volume', methods=['GET'])
    @token_required
    def get_results():
        try:
            return jsonify(stored_results), 200
        except Exception as e:
            return jsonify({"message": "An error occurred while retrieving results", "error": str(e)}), 500
