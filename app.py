from flask import Flask, request
from src.config import Config
from apscheduler.schedulers.background import BackgroundScheduler
from src.services.external_api_service import fetch_and_process_data
from src.blueprints.calculation_bp import create_calculation_routes
from flask_pymongo import PyMongo
from datetime import datetime
import os
import logging
from src.utils_backend import logging_report, ENVIRONMENT

app = Flask(__name__)
app.config.from_object(Config)

mongo = PyMongo(app)

def create_app():
    with app.app_context():
        scheduler = BackgroundScheduler()
        scheduler.add_job(func=fetch_and_process_data, trigger="interval", minutes=5)
        scheduler.start()

        create_calculation_routes(app, mongo)

        return app

@app.before_request
def before_request_func():
    logpath = '/home/ubuntu/log/prodanalytics_wellbore/requests' if ENVIRONMENT == 'development' else '/mnt/log/prodanalytics_wellbore/requests'

    urlstring = request.url
    api_name = urlstring.split("enovate.app/")[1].split("/")[0] if "enovate.app" in urlstring else "URL_ERROR"
    save_path = f'{logpath}/{api_name}/'

    if not os.path.exists(save_path):
        os.makedirs(save_path)

    log_date = datetime.now().strftime("%Y%m%d")
    source_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    log_entry = f'{source_ip} {datetime.now()} REQUEST {request.method} {request.url}'
    
    logging_report(log_entry, 'INFO', api_name)

@app.after_request
def after_request_func(response):
    logpath = '/home/ubuntu/log/prodanalytics_wellbore/requests' if ENVIRONMENT == 'development' else '/mnt/log/prodanalytics_wellbore/requests'

    urlstring = request.url
    api_name = urlstring.split("enovate.app/")[1].split("/")[0] if "enovate.app" in urlstring else "URL_ERROR"
    save_path = f'{logpath}/{api_name}/'

    if not os.path.exists(save_path):
        os.makedirs(save_path)

    log_date = datetime.now().strftime("%Y%m%d")
    source_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    log_entry = f'{source_ip} {datetime.now()} RESPONSE {request.method} {request.url} {response.status}'
    
    logging_report(log_entry, 'INFO', api_name)

    return response

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
