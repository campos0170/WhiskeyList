from flask import Flask
from flask_cors import CORS
from .config import Config
from .database import db
from flask_jwt_extended import JWTManager

jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    jwt.init_app(app)
    CORS(app)

    from .auth import auth
    from .routes import whiskey_routes

    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(whiskey_routes, url_prefix='/whiskeys')

    return app
