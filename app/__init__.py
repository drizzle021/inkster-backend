from flask import Flask
from app.extensions import db, migrate, jwt
from app.routes import register_routes
from app.config import Config
from app.models import *



def create_app(config_class=Config):
    app = Flask(__name__)

    app.config.from_object(config_class)
    
    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)

    register_routes(app)

    return app