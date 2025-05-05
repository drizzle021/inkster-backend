from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_socketio import SocketIO

db = SQLAlchemy()
jwt = JWTManager()
migrate = Migrate()
socketio = SocketIO()