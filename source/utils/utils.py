from flask import current_app, request, jsonify
from source.models.user_model import MongoDB
import jwt
from functools import wraps

def get_mongo():
    return MongoDB(uri=current_app.config['MONGO_URI'], db_name=current_app.config['MONGO_DB_NAME'])

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            if auth_header.startswith('Bearer '):
                token = auth_header.split(" ")[1]

        if not token:
            return jsonify({"message": "Token is missing!"}), 401

        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
            request.user_email = data['email']
        except Exception as e:
            return jsonify({"message": "Token is invalid!", "error": str(e)}), 401

        return f(*args, **kwargs)
    return decorated