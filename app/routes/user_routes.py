from flask import Blueprint, request, jsonify
from app.services.user_service import UserService
from flask_jwt_extended import jwt_required, get_jwt_identity

user_bp = Blueprint("users", __name__)

@user_bp.route("/users", methods=["GET"])
def get_users():
    """
    Route to retrieve all users, with optional filtering:
        - ?keywords=...
        - ?tags=tag1,tag2,...
    """

    keywords = request.args.get("keywords")
    raw_tags = request.args.get("tags", "")
    tag_list = [tag.strip() for tag in raw_tags.split(",") if tag.strip()]

    response, status_code = UserService.get_all_users(keywords=keywords, tags=tag_list)
    
    return jsonify(response), status_code

@user_bp.route("/users/<int:id>", methods=["GET"])
@jwt_required()
def get_user(id):
    """
    Route to retrieve a user with a specific ID
    """

    response, status_code = UserService.get_user(id)
    
    return jsonify(response), status_code

@user_bp.route("users/me", methods=["GET"])
@jwt_required()
def me():
    """
    Route to retrieve the current user
    """

    id = get_jwt_identity()

    response, status_code = UserService.get_user(id)
    
    return jsonify(response), status_code

@user_bp.route("/users/update-pictures", methods=["PUT"])
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


@user_bp.route("/users/update-tags", methods=["PUT"])
@jwt_required()
def update_user_tags():
    """
    Route to update tags associated with the user.
    """
    identity = get_jwt_identity()
    raw_tags = request.form.get("tags", "") 
    tag_list = [t.strip().lower() for t in raw_tags.split(",") if t.strip()]

    response, status_code = UserService.update_tags(identity, tag_list)
    return jsonify(response), status_code


@user_bp.route("/users/saved", methods=["GET"])
@jwt_required()
def get_my_saved_posts():
    identity = get_jwt_identity()
    response, status = UserService.get_saved_posts(user_id=identity)
    return jsonify(response), status

@user_bp.route("/users/follow/<int:id>", methods=["POST"])
@jwt_required()
def follow(id):
    identity = get_jwt_identity()

    response, status = UserService.toggle_follow(id, identity)
    return jsonify(response), status

@user_bp.route("/users/image/<name>", methods=["GET"])
@jwt_required()
def get_image(name):
    response, status_code = UserService.get_image(name)

    if status_code == 200:
        return response, status_code

    return jsonify(response), status_code


@user_bp.route("/users/fcm-token", methods=["POST"])
@jwt_required()
def get_fcm_token():
    identity = get_jwt_identity()
    data = request.get_json()
    fcm_token = data.get("token")
    print(fcm_token)
    if not fcm_token:
        return jsonify({"error": "FCM token is required"}), 400

    response, status_code = UserService.save_fcm(identity, fcm_token)
    return jsonify(response), status_code