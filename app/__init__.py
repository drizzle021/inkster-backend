from flask import Flask
from app.extensions import db, migrate, jwt, socketio
from app.routes import register_routes
from app.config import Config
from app.models import *
from flask_cors import CORS
from flask_socketio import SocketIO
import firebase_admin
from firebase_admin import credentials

def create_app(config_class=Config):
    app = Flask(__name__)
    CORS(app)

    app.config.from_object(config_class)
    
    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)
    socketio.init_app(app, cors_allowed_origins="*")

    cred = credentials.Certificate("inkster-e3441-firebase-adminsdk-fbsvc-c7546aed32.json")

    firebase_admin.initialize_app(cred)

    from app import sockets
    register_routes(app)

    return app





