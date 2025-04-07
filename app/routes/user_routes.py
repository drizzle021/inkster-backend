from flask import Blueprint, request, jsonify
from app.services.user_service import UserService
from app.services.post_service import PostService
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


@user_bp.route("/users/follow/<int:id>", methods=["POST"])
@jwt_required()
def follow_user(id):
    """
    Route to follow a user with a specific ID
    """
    identity = get_jwt_identity()

    response, status_code = UserService.toggle_follow(id, identity)
    
    return jsonify(response), status_code



@user_bp.route("/users/saved", methods=["GET"])
@jwt_required()
def get_my_saved_posts():
    identity = get_jwt_identity()
    response, status = UserService.get_saved_posts(user_id=identity)
    return jsonify(response), status


