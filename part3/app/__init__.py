from flask import Flask
from app.api import api


def create_app(config_class="config.DevelopmentConfig"):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    api.init_app(app)
    return app
