from flask import Blueprint, request, jsonify
from app.services.user_service import UserService

user_bp = Blueprint("users", __name__)

@user_bp.route("/users", methods=["GET"])
def get_users():
    """
    Route to retrieve all users.
    """
    return jsonify(UserService.get_all_users()), 200
