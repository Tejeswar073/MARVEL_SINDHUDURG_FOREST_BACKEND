from flask import request, Blueprint, jsonify
from source.models.user_model import MongoDB
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import jwt

from source.utils import utils

auth_bp = Blueprint("auth_bp",__name__)

@auth_bp.route('signin',methods=['POST'])
def signin_route():
    
    if 'email' not in request.json:
        return jsonify({"message":"Field email not found"}), 404
    
    if 'password' not in request.json:
        return jsonify({"message":"Field password not found"}), 404
    
    mongo = utils.get_mongo()
    
    user_details = request.json
    
    user_email = user_details.get('email')
    user_pass = user_details.get('password')
    user = mongo.users.find_one({"email": email})
    
    secret_key = current_app.config['SECRET_KEY']
    
    if not user:
        return jsonify({"success": False, "message": "Email not registered."}), 400
    
    if not check_password_hash(user["password"], password):
        return jsonify({"success": False, "message": "Incorrect password."}), 400
    
    payload = {
        "email": email,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }
    access_token = jwt.encode(payload, secret_key, algorithm="HS256")

    # Prepare response with headers
    response = make_response(jsonify({"message": "Login successful"}), 200)
    response.headers["Authorization"] = f"Bearer {access_token}"
    response.headers["Access-Control-Expose-Headers"] = "Authorization"

    return response

@auth_bp.route('create_user',methods=['POST'])
def create_user_route():
    
    if 'email' not in request.json:
        return jsonify({"message":"Field email not found"}), 404
    
    if 'password' not in request.json:
        return jsonify({"message":"Field password not found"}), 404
    
    email = request.json.get('email')
    password = request.json.get('password')
    name = request.json.get('user_name')
    mobile_number = request.json.get('mobile_number')
    taluka = request.json.get('taluka')
    range_ = request.json.get('range')
    round_ = request.json.get('round')
    beat = request.json.get('beat')
    role = request.json.get('role')
    state = request.json.get('state')
    district = request.json.get('district')
    created_by = request.json.get('created_by')
    created_on = datetime.now()
    status = request.json.get('status')
    type_ = request.json.get('type')
    region = request.json.get('region')
    
    mongo = utils.get_mongo()
    
    
    if mongo.users.find_one({"email": email}):
        return jsonify({"success": False, "message": "Email already registered."}), 400

    hashed_password = generate_password_hash(password)
    mongo.users.insert_one({
        "email": email,
        "password": hashed_password,
        "name":user_name,
        "mobile_nubmber":mobile_number,
        "taluke":taluka,
        "range":range_,
        "round":round_,
        "beat":beat,
        "role":role,
        "state":state,
        "district":district,
        "created_by":created_by,
        "created_on":created_on,
        "type":type_,
        "region":region,
        "status":status
    })
    
    return jsonify({'message':"success","user_details":{"email":user_email,"password":user_pass}}), 200

@auth_bp.route('update_user',methods=['POST'])
def update_route():
    
    if 'email' not in request.json:
        return jsonify({"message":"Field email not found"}), 404
    
    if 'admin' not in request.json:
        return jsonify({"message":"Field email not found"}), 404
    
    mongo = utils.get_mongo()
    
    user_details = request.json
    
    user_email = user_details.get('email')
    
    if not user:
        return jsonify({"success": False, "message": "Email not registered."}), 400
    
    if not check_password_hash(user["password"], password):
        return jsonify({"success": False, "message": "Incorrect password."}), 400
    
    return jsonify({'message':"success","user_details":{"email":user_email,"password":user_pass}}), 200