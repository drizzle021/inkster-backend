from flask import Blueprint, request, jsonify
from app.services.post_service import PostService
from app.models.post import PostType

post_bp = Blueprint("posts", __name__)

@post_bp.route("/posts", methods=["GET"])
def get_posts():
    """
    Route to retrieve all posts.
    """

    response, status_code = PostService.get_all_posts()
    
    return jsonify(response), status_code


# divide into novel and illustration maybe
@post_bp.route("/posts", methods=["POST"])
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

    # PICTURES in array? LAZY LOAD
    # picture = request.form.get()

    # check required fields
    if not title or not post_type or not caption:
        return jsonify({"error": "Missing required fields"}), 400

    response, status_code = PostService.add_post(title, post_type, caption, description, is_spoilered, software)

    return jsonify(response), status_code


@post_bp.route("/posts/<int:id>", methods=["GET"])
def get_post(id):
    """
    Route to retrieve a post with a specific ID.
    """

    response, status_code = PostService.get_post(id)

    return jsonify(response), status_code



@post_bp.route("/posts/<int:id>", methods=["DELETE"])
def delete_post(id):
    """
    Route to delete a post with a specific ID.
    """
    pass

@post_bp.route("/posts/<int:id>/report", methods=["POST"])
def report_post(id):
    """
    Route to report a post with a specific ID.
    """
    pass

@post_bp.route("/posts/<int:id>/edit", methods=["PUT"])
def edit_post(id):
    """
    Route to edit a post with a specific ID.
    """
    pass

# NO IDEA
@post_bp.route("/posts/<int:id>/like", methods=["POST"])
def like_post(id):
    """
    Route to add a like to a post with a specific ID.
    """
    pass

@post_bp.route("/posts/<int:id>/save", methods=["POST"])
def save_post(id):
    """
    Route to save a post with a specific ID to saved posts.
    """
    pass


@post_bp.route("/posts/<int:id>/comments", methods=["GET"])
def get_comments(id):
    """
    Route to retrieve all comments a post with a specific ID.
    """
    pass

@post_bp.route("/posts/<int:id>/comments", methods=["POST"])
def add_comment(id):
    """
    Route to add a comment to a post with a specific ID.
    """
    pass



