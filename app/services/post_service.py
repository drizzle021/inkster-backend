from app.models import Post, User, Like, Comment
from app.extensions import db
from app.models.user import saved_posts
from sqlalchemy import or_, and_
from app.models.post import PostType


class PostService:
    @staticmethod
    # pagination here maybe
    def get_all_posts(keywords=None, tags=None, post_type=None):
        """
        Retrieves all posts from the database.
        """

        filters = []

        if keywords:
            keyword_filter = or_(
                Post.title.ilike(f"%{keywords}%"),
                Post.caption.ilike(f"%{keywords}%"),
                Post.description.ilike(f"%{keywords}%")
            )
            filters.append(keyword_filter)
        
        if post_type:
            try:
                filters.append(Post.post_type == PostType(post_type.upper()))
            except ValueError:
                return {"error": f"Invalid post_type: {post_type}"}, 400        
            
        # TODO: TAGS
        # if tags:
        #     try:
        #         filters.append(Post.tags == PostType(post_type.upper()))
        #     except ValueError:
        #         return {"error": f"Invalid post_type: {post_type}"}, 400     

        print(filters)
        posts = Post.query.filter(and_(*filters)).all()


        return [
            {
            "id": post.id,
            "title": post.title,
            "post_type": post.post_type.name,
            "caption": post.caption,
            "description": post.description,
            "is_spoilered": post.is_spoilered,
            "software": post.software,
            "author": post.author_id
            }
            for post in posts
        ], 200
    
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
            "title": post.title,
            "post_type": post.post_type.name,
            "caption": post.caption,
            "description": post.description,
            "is_spoilered": post.is_spoilered,
            "software": post.software,
            "author": post.author_id

        }, 200


    @staticmethod
    def add_post(title, post_type, caption, description, is_spoilered, software, identity):
        """
        Creates a post in the database.

        Args:
            title
            post_type
            caption
            description
            is_spoilered
            software
        """



        # TODO: ADD PICTURES
        post = Post(
            title=title,
            post_type=post_type,
            caption=caption,
            description=description,
            is_spoilered=is_spoilered,
            software=software,
            author_id=identity
        )

        db.session.add(post)
        db.session.commit()

        return {"message": "New post created successfully"}, 201


    @staticmethod
    def delete_post(id, identity):
        """
        Deletes a post in the database.

        """

        post = db.session.get(Post, id)
        if not post:
            return {"error": "Post not found"}, 404
        
        
        logged_in_user = db.session.get(User, identity)

        if logged_in_user.id == post.author_id or logged_in_user.role.name == "MODERATOR":
            db.session.delete(post)
            db.session.commit()
            return {"message": "Post deleted successfully"}, 201

        else:
            return {"error": "Unauthorized"}, 401

    @staticmethod
    def edit_post(id, identity, data):
        """
        Edits a post in the database.

        """

        post = db.session.get(Post, id)
        if not post:
            return {"error": "Post not found"}, 404
        
        
        logged_in_user = db.session.get(User, identity)


        if logged_in_user.id != post.author_id:
            return {"error": "Unauthorized"}, 401

        # Only update if value is provided and not empty
        if "title" in data and data["title"].strip() != "":
            post.title = data["title"].strip()

        if "caption" in data and data["caption"].strip() != "":
            post.caption = data["caption"].strip()

        if "description" in data and data["description"].strip() != "":
            post.description = data["description"].strip()

        if "software" in data and data["software"].strip() != "":
            post.software = data["software"].strip()

        # Handle boolean
        if "is_spoilered" in data:
            raw = data["is_spoilered"]
            if isinstance(raw, bool):
                post.is_spoilered = raw
            elif isinstance(raw, str):
                post.is_spoilered = raw.lower() == "true"

        db.session.commit()
        return {"message": "Post updated successfully"}, 200
    
    
    @staticmethod
    def toggle_like(post_id, user_id):
        """
        Toggles like for a post: adds like if not liked, removes like if already liked.
        """
        post = db.session.get(Post, post_id)
        if not post:
            return {"error": "Post not found"}, 404

        existing_like = Like.query.filter_by(post_id=post_id, user_id=user_id).first()

        if existing_like:
            db.session.delete(existing_like)
            db.session.commit()
            return {"message": "Post unliked"}, 200

        new_like = Like(post_id=post_id, user_id=user_id)
        db.session.add(new_like)
        db.session.commit()
        return {"message": "Post liked"}, 200

    @staticmethod
    def add_comment(post_id, user_id, content):
        """
        Creates comment for a Post in database
        """
        post = db.session.get(Post, post_id)
        if not post:
            return {"error": "Post not found"}, 404

        comment = Comment(post_id=post_id, author_id=user_id, content=content)

        db.session.add(comment)
        db.session.commit()

        return {"message": "Comment added successfully"}, 201
    
    @staticmethod
    # pagination here maybe
    def get_comments(id):
        """
        Retrieves all comments for a Post from the database.
        """
        post = db.session.get(Post, id)
        if not post:
            return {"error": "Post not found"}, 404
        
        comments = Comment.query.filter_by(post_id=id).order_by(Comment.created_at.asc()).all()

        return [
            {
                "id": comment.id,
                "content": comment.content,
                "author_id": comment.author_id,
                "post_id": comment.post_id,
                "created_at": comment.created_at
            }
            for comment in comments
        ], 200

    @staticmethod
    def toggle_save(post_id, user_id):
        """
        Toggles save for a post: adds save if not saved, removes save if already saved.
        """
        post = db.session.get(Post, post_id)
        if not post:
            return {"error": "Post not found"}, 404

        # existing_save = User.query.filter_by(post_id=post_id, user_id=user_id).first()

        exists = db.session.execute(
            db.select(saved_posts).where(
                saved_posts.c.user_id == user_id,
                saved_posts.c.post_id == post_id
            )
        ).first()

        if exists:
            # Unsave it
            db.session.execute(
                saved_posts.delete().where(
                    saved_posts.c.user_id == user_id,
                    saved_posts.c.post_id == post_id
                )
            )
            db.session.commit()
            return {"message": "Post unsaved successfully"}, 200

        db.session.execute(
            saved_posts.insert().values(user_id=user_id, post_id=post_id)
        )
        db.session.commit()
        return {"message": "Post saved successfully"}, 200
