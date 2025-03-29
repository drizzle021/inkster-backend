from app.models import Post
from app.extensions import db

class PostService:
    @staticmethod
    # pagination here maybe
    def get_all_posts():
        """
        Retrieves all posts from the database.
        """
        posts = Post.query.all()
        return [
            {
                "id": post.id,
            }
            for post in posts
        ]
    
    @staticmethod
    def get_post(id):
        """
        Retrieves a specific post from the database.

        Args:
        
            id (int): ID of the post to be retrieved.
        """
        post = db.session.get(Post, id)
        if not post:
            return {"error": "Post not found"}, 404
        
        return {
            "id": post.id,

        }, 200


