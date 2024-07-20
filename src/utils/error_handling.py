from functools import wraps
from flask import jsonify

def handle_errors(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            response = jsonify({"error": str(e)})
            response.status_code = 500
            return response
    return decorated_function
