from flask import Flask
from flask_pymongo import PyMongo
from src.config import Config
from apscheduler.schedulers.background import BackgroundScheduler
from src.services.external_api_service import fetch_and_process_data
from src.routes.calculation_routes import create_calculation_routes

app = Flask(__name__)
app.config.from_object(Config)

mongo = PyMongo(app)

def create_app():
    with app.app_context():
        scheduler = BackgroundScheduler()
        scheduler.add_job(func=fetch_and_process_data, trigger="interval", minutes=5, args=[mongo])
        scheduler.start()

        create_calculation_routes(app, mongo)
        
        return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
