from flask import Flask 
from dotenv import load_dotenv
import os
from flask_cors import CORS

from source.routes.auth.routes_auth import auth_bp
from source.routes.parser.route_parser import parser_bp

def create_app():
    load_dotenv()
    
    app = Flask(__name__)
    
    CORS(app)
    
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['MONGO_URI'] = os.getenv('MONGO_URI')
    app.config['MONGO_DB_NAME'] = os.getenv('MONGO_DB_NAME')
    
    app.register_blueprint(auth_bp,url_prefix='/auth')
    app.register_blueprint(parser_bp,url_prefix='/parser')
    
    return app