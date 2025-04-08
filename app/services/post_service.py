from app.models import Post, User, Like, Comment, Tag
from app.extensions import db
from app.models.user import saved_posts
from sqlalchemy import or_, and_
from app.models.post import PostType


class PostService:

    # pagination here maybe
    @staticmethod
    def get_all_posts(keywords=None, tags=None, post_type=None):
        """
        Retrieves all posts from the database, with optional filters:
            - keywords (in title, caption, or description)
            - post_type (ILLUSTRATION, MANGA, NOVEL)
            - tags (matches posts having ANY of the given tag names)
        """

        print(tags)
        filters = []

        # Keyword search
        if keywords:
            keyword_filter = or_(
                Post.title.ilike(f"%{keywords}%"),
                Post.caption.ilike(f"%{keywords}%"),
                Post.description.ilike(f"%{keywords}%")
            )
            filters.append(keyword_filter)

        # Post type filter
        if post_type:
            try:
                filters.append(Post.post_type == PostType(post_type.upper()))
            except ValueError:
                return {"error": f"Invalid post_type: {post_type}"}, 400

        posts_query = Post.query

        # Tag filter
        if tags:
            tag_names = [tag.strip().lower() for tag in tags if tag.strip()]
            if tag_names:
                posts_query = posts_query.join(Post.tags).filter(Tag.name.in_(tag_names)).distinct()

        if filters:
            posts_query = posts_query.filter(and_(*filters))

        posts = posts_query.all()

        return [
            {
                "id": post.id,
                "title": post.title,
                "post_type": post.post_type.name,
                "caption": post.caption,
                "description": post.description,
                "is_spoilered": post.is_spoilered,
                "software": post.software,
                "author": post.author_id,
                "tags": [tag.name for tag in post.tags]
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
            "author": post.author_id,
            "tags": [tag.name for tag in post.tags]

        }, 200


    @staticmethod
    def add_post(title, post_type, caption, description, is_spoilered, software, identity, tag_list):
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
            author_id=identity,
        )


        if tag_list:
            tags = []  
            for tag_name in tag_list:
                tag = Tag.query.filter_by(name=tag_name).first()
                if not tag:
                    tag = Tag(name=tag_name)
                    db.session.add(tag)
                tags.append(tag)
            
            post.tags = tags


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


        # Handle tags
        tag_names = []
        if "tags" in data:
            # If sent as comma-separated
            raw_tags = data.get("tags")
            if isinstance(raw_tags, str):
                tag_names = [tag.strip().lower() for tag in raw_tags.split(",") if tag.strip()]
            
            # If sent as list of tags (form.getlist())
            elif isinstance(raw_tags, list):
                tag_names = [tag.strip().lower() for tag in raw_tags if tag.strip()]

            tags = []
            for tag_name in tag_names:
                tag = Tag.query.filter_by(name=tag_name).first()
                if not tag:
                    tag = Tag(name=tag_name)
                    db.session.add(tag)
                tags.append(tag)

            post.tags = tags  # Replace old tags with new ones

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
