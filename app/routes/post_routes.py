from flask import Blueprint, request, jsonify
from app.services.post_service import PostService
from app.services.report_service import ReportService
from app.models.post import PostType
from flask_jwt_extended import jwt_required, get_jwt_identity

post_bp = Blueprint("posts", __name__)

@post_bp.route("/posts", methods=["GET"])
@jwt_required()
def get_posts():
    """
    Route to retrieve all posts.
    """

    response, status_code = PostService.get_all_posts()
    
    return jsonify(response), status_code


# divide into novel and illustration maybe

@post_bp.route("/posts", methods=["POST"])
@jwt_required()
def add_post():
    """
    Route to create a new post
    """

    title = request.form.get("title")
    post_type = request.form.get("post_type")
    post_type = PostType(post_type)
    caption = request.form.get("caption")
    description = request.form.get("description")
    is_spoilered = request.form.get("is_spoilered", "false").lower() == "true"
    software = request.form.get("software")

    identity = get_jwt_identity()
    print(f"IDENTITY {identity}")

    # PICTURES in array? LAZY LOAD
    # picture = request.form.get()

    # check required fields
    if not title or not post_type or not caption:
        return jsonify({"error": "Missing required fields"}), 400

    response, status_code = PostService.add_post(title, post_type, caption, description, is_spoilered, software, identity)

    return jsonify(response), status_code


@post_bp.route("/posts/<int:id>", methods=["GET"])
@jwt_required()
def get_post(id):
    """
    Route to retrieve a post with a specific ID.
    """

    response, status_code = PostService.get_post(id)

    return jsonify(response), status_code



@post_bp.route("/posts/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_post(id):
    """
    Route to delete a post with a specific ID.
    """
    identity = get_jwt_identity()
    response, status_code = PostService.delete_post(id, identity)

    return jsonify(response), status_code


@post_bp.route("/posts/<int:id>/report", methods=["POST"])
@jwt_required()
def report_post(id):
    """
    Route to report a post with a specific ID.
    """

    report_type = request.form.get("report_type")

    description = request.form.get("description")

    identity = get_jwt_identity()

    # check required fields
    if not description or not report_type:
        return jsonify({"error": "Missing required fields"}), 400

    response, status_code = ReportService.add_report(id, report_type, description, identity)

    return jsonify(response), status_code


@post_bp.route("/posts/<int:id>/edit", methods=["PUT"])
@jwt_required()
def edit_post(id):
    """
    Route to edit a post with a specific ID.
    """
    identity = get_jwt_identity()
    data = request.form

    response, status_code = PostService.edit_post(id, identity, data)

    return jsonify(response), status_code



# NO IDEA
@post_bp.route("/posts/<int:id>/like", methods=["POST"])
@jwt_required()
def like_post(id):
    """
    Route to add a like to a post with a specific ID.
    """
    identity = get_jwt_identity()
    response, status_code = PostService.toggle_like(id, identity)
    return jsonify(response), status_code



@post_bp.route("/posts/<int:id>/save", methods=["POST"])
@jwt_required()
def save_post(id):
    """
    Route to save a post with a specific ID to saved posts.
    """
    identity = get_jwt_identity()
    response, status = PostService.save_post(id, identity)
    return jsonify(response), status

@post_bp.route("/posts/<int:id>/save", methods=["DELETE"])
@jwt_required()
def unsave_post(id):
    identity = get_jwt_identity()
    response, status = PostService.unsave_post(id, identity)
    return jsonify(response), status





@post_bp.route("/posts/<int:id>/comments", methods=["GET"])
@jwt_required()
def get_comments(id):
    """
    Route to retrieve all comments a post with a specific ID.
    """
    response, status = PostService.get_comments(id)
    return jsonify(response), status

@post_bp.route("/posts/<int:id>/comments", methods=["POST"])
@jwt_required()
def add_comment(id):
    """
    Route to add a comment to a post with a specific ID.
    """
    identity = get_jwt_identity()
    content = request.form.get("content")

    if not content or content.strip() == "":
        return jsonify({"error": "Comment content is required"}), 400
    
    response, status_code = PostService.add_comment(id, identity, content.strip())
    return jsonify(response), status_code


@post_bp.route("/posts/search", methods=["GET"])
@jwt_required()
def search_post():
    """
    Route to search for posts with filter.
    """
    pass
