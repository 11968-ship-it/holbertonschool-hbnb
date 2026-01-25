from flask import Flask
from app.api import api
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy

jwt = JWTManager()

bcrypt = Bcrypt()

db = SQLAlchemy()

def create_app(config_class="config.DevelopmentConfig"):
    app = Flask(__name__)
    app.config.from_object(config_class)

    bcrypt.init_app(app)
    api.init_app(app)
    jwt.init_app(app)
    db.init_app(app)
    return app
