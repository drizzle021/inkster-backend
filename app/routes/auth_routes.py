from flask import Blueprint, request, jsonify
from app.services.auth_service import AuthService

auth_bp = Blueprint("auth", __name__)


@auth_bp.route('/', methods=['GET'])
def hello():
    return jsonify({"hello": "world"}), 200


@auth_bp.route('/register', methods=['POST'])
def register():
    """
    Route to register a new user in the system.
    """
    data = request.get_json()

    # check required fields
    if not all(key in data for key in ["username", "email", "password"]):
        return jsonify({"error": "Missing required fields"}), 400

    response, status_code = AuthService.register_user(data)

    return jsonify(response), status_code


@auth_bp.route("/login", methods=["POST"])
def login():
    """
    Route to authenticate a user and return a token.
    """
    data = request.get_json()

    if not all(key in data for key in ["email", "password"]):
        return jsonify({"error": "Missing required fields"}), 400

    response, status_code = AuthService.authenticate_user(data)
    
    return jsonify(response), status_code