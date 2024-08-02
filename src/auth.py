from functools import wraps
from flask import request, jsonify
from src.config import Config

def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token or token != f"Token {Config.INTERNAL_API_TOKEN}":
            return jsonify({"message": "Unauthorized"}), 403
        return f(*args, **kwargs)
    return decorated_function
