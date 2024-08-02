from flask import Blueprint
from src.controllers.calculation_controller import register_calculation_routes

def create_calculation_routes(app, mongo):
    calculation_bp = Blueprint('calculation_bp', __name__)
    register_calculation_routes(calculation_bp, mongo)
    app.register_blueprint(calculation_bp)
