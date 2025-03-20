from flask import Blueprint, request, jsonify
from app.services.user_service import create_user, get_all_users

user_bp = Blueprint("users", __name__)

@user_bp.route("/users", methods=["POST"])
def add_user():
    """
    Route to create a new user.
    """
    data = request.get_json()
    if not all(key in data for key in ["username", "email", "password", "profile_picture", "banner"]):
        return jsonify({"error": "Missing required fields"}), 400
    return create_user(data)


@user_bp.route("/users", methods=["GET"])
def get_users():
    """
    Route to retrieve all users.
    """
    return jsonify(get_all_users()), 200
