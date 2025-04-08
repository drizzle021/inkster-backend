from flask import Blueprint, request, jsonify
from app.services.user_service import UserService
from flask_jwt_extended import jwt_required, get_jwt_identity

user_bp = Blueprint("users", __name__)

@user_bp.route("/users", methods=["GET"])
def get_users():
    """
    Route to retrieve all users.
    """

    response, status_code = UserService.get_all_users()
    
    return jsonify(response), status_code

@user_bp.route("/users/<int:id>", methods=["GET"])
def get_user(id):
    """
    Route to retrieve a user with a specific ID
    """

    response, status_code = UserService.get_user(id)
    
    return jsonify(response), status_code



@user_bp.route("/users/update-pictures/", methods=["PUT"])
@jwt_required()
def update_pictures():
    """
    Route to update the user's profile picture or banner from a frontend
    """

    if "profile_picture" not in request.files and "banner" not in request.files:
        return jsonify({"error": "At least one of profile picture or banner must be provided"}), 400


    id = get_jwt_identity()
    profile_picture = request.files.get("profile_picture")
    banner = request.files.get("banner")

    response, status_code = UserService.update_pictures(id, profile_picture, banner)

    return jsonify(response), status_code


@user_bp.route("/users/saved", methods=["GET"])
@jwt_required()
def get_my_saved_posts():
    identity = get_jwt_identity()
    response, status = UserService.get_saved_posts(user_id=identity)
    return jsonify(response), status


