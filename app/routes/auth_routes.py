from flask import Blueprint, jsonify
# from app.services.auth_service import AuthService

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/', methods=['GET'])
def hello():
    return jsonify({"hello": "world"}), 200


@auth_bp.route('/register', methods=['POST'])
def register():
    pass