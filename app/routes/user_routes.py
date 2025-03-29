from flask import Blueprint, request, jsonify
from app.services.user_service import UserService

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


@user_bp.route("/users/<int:id>/update-pictures", methods=["PUT"])
def update_pictures(id):
    """
    Route to update the user's profile picture or banner
    """

    files = request.files
    
    if "profile_picture" not in files and "banner" not in files:
        return jsonify({"error": "At least one of 'profile_picture' or 'banner' must be provided"}), 400
    

    response, status_code = UserService.update_pictures(files)
    
    return jsonify(response), status_code


@user_bp.route("/users/<int:id>", methods=["POST"])
def follow_user(id):
    """
    Route to follow a user with a specific ID
    """

    response, status_code = UserService.get_user(id)
    
    return jsonify(response), status_code








