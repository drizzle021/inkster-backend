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
    
    Required fields: username, email, password
    """
    username = request.form.get("username")
    email = request.form.get("email")
    password = request.form.get("password")

    # check required fields
    if not username or not email or not password:
        return jsonify({"error": "Missing required fields"}), 400
    

    response, status_code = AuthService.register_user(username, email, password)

    return jsonify(response), status_code


@auth_bp.route("/login", methods=["POST"])
def login():
    """
    Route to authenticate a user and return a token.

    Required fields: email, password
    """
    email = request.form.get("email")
    password = request.form.get("password")

    if not email or not password:
        return jsonify({"error": "Missing required fields"}), 400

    response, status_code = AuthService.authenticate_user(email, password)
    
    return jsonify(response), status_code


@auth_bp.route("/logout", methods=["POST"])
def logout():
    """
    Route to logout a user.

    """
    # logout_user()
    
    return jsonify({"message": "Logged out successfully"}), 200