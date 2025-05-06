from flask import request, Blueprint, jsonify, current_app, make_response
from source.models.user_model import MongoDB
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
import jwt

auth_bp = Blueprint("auth_bp", __name__)

def get_mongo():
    return MongoDB(
        uri=current_app.config['MONGO_URI'],
        db_name=current_app.config['MONGO_DB_NAME']
    )

@auth_bp.route('/signin', methods=['POST'])
def signin_route():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"message": "Email and password are required"}), 400

    mongo = get_mongo()
    user = mongo.users.find_one({"email": email})
    if not user:
        return jsonify({"success": False, "message": "Email not registered."}), 400

    if not check_password_hash(user["password"], password):
        return jsonify({"success": False, "message": "Incorrect password."}), 400

    payload = {
        "email": email,
        "role": data['role'],
        "name": data['name'],
        "exp": datetime.utcnow() + timedelta(hours=1)
    }
    token = jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm="HS256")

    response = make_response(jsonify({"message": "Login successful"}), 200)
    response.headers["Authorization"] = f"Bearer {token}"
    response.headers["Access-Control-Expose-Headers"] = "Authorization"

    return response

@auth_bp.route('/createuser', methods=['POST'])
def create_user_route():
    data = request.json
    required_fields = ['name', 'email', 'password', 'role', 'region', 'status']
    for field in required_fields:
        if field not in data:
            return jsonify({"message": f"Field '{field}' not found"}), 400

    email = data['email']
    password = data['password']

    mongo = get_mongo()
    if mongo.users.find_one({"email": email}):
        return jsonify({"success": False, "message": "Email already registered."}), 400

    hashed_password = generate_password_hash(password)
    data['password'] = hashed_password
    data['created_on'] = datetime.now()

    mongo.users.insert_one(data)

    return jsonify({'message': "User created successfully", "user_email": email}), 200

@auth_bp.route('/update_user', methods=['PUT'])
def update_user_route():
    data = request.json
    email = data.get('email')
    if not email:
        return jsonify({"message": "Field 'email' is required for update"}), 400

    mongo = get_mongo()
    user = mongo.users.find_one({"email": email})
    if not user:
        return jsonify({"success": False, "message": "User not found"}), 404

    update_fields = {}
    for key, value in data.items():
        if key == 'email':
            continue
        elif key == 'password':
            update_fields['password'] = generate_password_hash(value)
        else:
            update_fields[key] = value

    if not update_fields:
        return jsonify({"message": "No fields provided for update"}), 400

    mongo.users.update_one({"email": email}, {"$set": update_fields})

    return jsonify({"message": "User updated successfully", "updated_fields": list(update_fields.keys())}), 200
