from flask import Flask
from app.extensions import db, jwt
from app.routes import register_routes
from app.config import Config

def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)
    
    db.init_app(app)
    jwt.init_app(app)

    register_routes(app)

    return app