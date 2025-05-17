#__init__.py
import os
from flask import Flask
from flask_cors import CORS
from .config import Config
from .database import db
import firebase_admin
from firebase_admin import credentials

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    
    cred_path = "/Users/abrahamcampos/Desktop/whiskey-app/backend/firebase/whiskeylistapp-firebase-adminsdk-fbsvc-94d62dc20e.json"

    cred = credentials.Certificate(cred_path)
    firebase_admin.initialize_app(cred)

    
    db.init_app(app)
    CORS(app)

   
    from .auth import auth
    from .routes import whiskey_routes

    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(whiskey_routes, url_prefix='/whiskeys')

    @app.route('/')
    def index():
        return {'message': 'Welcome to the Whiskey API'}, 200

    return app
