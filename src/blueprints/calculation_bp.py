from flask import Blueprint
from src.controllers.calculation_controller import register_calculation_routes

calculation_bp = Blueprint('calculation_bp', __name__)

def create_calculation_routes(app, mongo):
    register_calculation_routes(calculation_bp, mongo)
    app.register_blueprint(calculation_bp)
