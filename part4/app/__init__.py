from flask import Flask
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

jwt = JWTManager()
bcrypt = Bcrypt()
db = SQLAlchemy()

def create_app(config_class="config.DevelopmentConfig"):
    app = Flask(__name__)
    app.config.from_object(config_class)

    app.url_map.strict_slashes = False
    
    CORS(app, resources={
        r"/api/*": {
            "origins": ["http://127.0.0.1:5000", "http://localhost:5000", "http://127.0.0.1:5501", "*"],
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"],
            "expose_headers": ["Content-Type", "Authorization"],
            "supports_credentials": True,
            "max_age": 3600
        }
    })

    bcrypt.init_app(app)
    jwt.init_app(app)
    db.init_app(app)

    # Import models
    from app.models.user import User
    from app.models.place import Place
    from app.models.review import Review
    from app.models.amenity import Amenity

    from app.api import api
    api.init_app(app)
    
    return app
