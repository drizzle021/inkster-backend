from app.models import User, Post, Tag, Image
from app.extensions import db
from werkzeug.utils import secure_filename
import os
from app.models.user import follows, saved_posts
from app.utils import encode_filename, validate_filename, validate_file_size, normalize_image
from flask import current_app, send_from_directory
from flask_jwt_extended import get_jwt_identity
from sqlalchemy import or_, and_

class UserService:
    @staticmethod
    def get_all_users(keywords=None, tags=None):
        """
        Retrieves all users from the database, with optional filters:
            - keywords (search in username)
            - tags (matches users having ANY of the given tag names)
        """
        filters = []

        # Keyword search
        if keywords:
            keyword_filter = User.username.ilike(f"%{keywords}%")
            filters.append(keyword_filter)

        users_query = User.query

        # Tag filter
        if tags:
            tag_names = [tag.strip().lower() for tag in tags if tag.strip()]
            if tag_names:
                users_query = users_query.join(User.tags).filter(Tag.name.in_(tag_names)).distinct()

        if filters:
            users_query = users_query.filter(and_(*filters))

        users = users_query.all()

        return [
            {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "profile_picture": user.profile_picture,
            }
            for user in users
        ], 200
    
    @staticmethod
    def get_user(id):
        """
        Retrieves a specific user from the database.

        Args:
        
            id (int): ID of the user to be retrieved.
        """
        user = db.session.get(User, id)
        if not user:
            return {"error": "User not found"}, 404
        
        followers = db.session.query(follows).filter(follows.c.followed_id == user.id).count()
        following = db.session.query(follows).filter(follows.c.follower_id == user.id).count()


        current_user_id = get_jwt_identity()

        is_following = False
        if current_user_id and current_user_id != user.id:
            follow_exists = db.session.execute(
                db.select(follows).where(
                    follows.c.followed_id == user.id,
                    follows.c.follower_id == current_user_id
                )
            ).first()
            is_following = bool(follow_exists)

        return {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "role": user.role.name,
            "profile_picture": user.profile_picture,
            "banner": user.banner,
            "tags": [tag.name for tag in user.tags],
            "following": following,
            "followers": followers,
            "is_following": is_following,
            "posts": [
                {
                    "id": post.id,
                    "title": post.title,
                    "post_type": post.post_type.name,
                    "caption": post.caption,
                    "description": post.description,
                    "is_spoilered": post.is_spoilered,
                    "software": post.software,
                    "created_at": post.created_at,
                    "thumbnail": post.images[0].image_name
                    
                } for post in user.posts
            ],
            

        }, 200
        

    @staticmethod
    def update_pictures(id, profile_picture, banner):
        """
        Updates the user's profile picture or banner

        """
        

        user = db.session.get(User, id)
        if not user:
            return {"error": "User not found"}, 404
        

        # validate if file is right format
        if profile_picture and not validate_filename(profile_picture.filename) or banner and not validate_filename(banner.filename) :
            return {"error": "Invalid file format"}, 400
        
        # folder has to be set up in .env and created
        # app/... /
        # default: app\static\uploads
        if not os.path.exists(current_app.config["UPLOAD_FOLDER"]):
            print(current_app.config["UPLOAD_FOLDER"])
            return {"error": "Server error: Upload folder does not exist"}, 500
        
        
        # encode filenames into Uuid4 -> Base64 + timestamp to avoid collisions
        # save pictures to storage and save filename to database
        if profile_picture:
            if not validate_file_size(profile_picture):
                return {"error": f"File size exceeds the limit for {profile_picture.filename}"}, 413

            normalized_image = normalize_image(profile_picture)
            encoded_filename = encode_filename(profile_picture.filename)
            user.profile_picture = encoded_filename 

            file_path = os.path.join(current_app.config["UPLOAD_FOLDER"], encoded_filename)

            with open(file_path, "wb") as f:
                f.write(normalized_image.read())


        if banner:
            if not validate_file_size(banner):
                return {"error": f"File size exceeds the limit for {banner.filename}"}, 413
            
            normalized_image = normalize_image(banner)
            encoded_filename = encode_filename(banner.filename)
            user.banner = encoded_filename

            file_path = os.path.join(current_app.config["UPLOAD_FOLDER"], encoded_filename)
            with open(file_path, "wb") as f:
                f.write(normalized_image.read())


        db.session.commit()
        return {"message": "Profile successfully updated"}, 200


    @staticmethod
    def update_tags(user_id, tag_list):
        user = db.session.get(User, user_id)
        if not user:
            return {"error": "User not found"}, 404

        new_tags = []
        for tag_name in tag_list:
            tag = Tag.query.filter_by(name=tag_name).first()
            if not tag:
                tag = Tag(name=tag_name)
                db.session.add(tag)
            new_tags.append(tag)

        user.tags = new_tags  # Replace all current tags
        db.session.commit()
        return {"message": "User tags updated successfully"}, 200


    @staticmethod
    def get_saved_posts(user_id):
        results = db.session.execute(
            db.select(Post, saved_posts.c.saved_at).join(saved_posts).where(saved_posts.c.user_id == user_id)
        ).all()


        return [
            {
                "id": post.id,
                "title": post.title,
                "post_type": post.post_type.name,
                "caption": post.caption,
                "is_spoilered": post.is_spoilered,
                "description": post.description,
                "thumbnail": post.images[0].image_name,
                "author_id": post.author_id,
                "author": {
                    "id": post.author.id,
                    "username": post.author.username,
                    "profile_picture": post.author.profile_picture,
                    "date_joined": post.author.date_joined,
                },
                "saved_at": saved_at,
                "created_at": post.created_at
            }
            for post, saved_at in results
        ], 200
    
    @staticmethod
    def toggle_follow(followed_id, follower_id):
        """
        Toggles follow for a user: adds follow if not followed, removes follow if already followed.
        """

        # ids remained in type string for some reason, leave in int
        if int(followed_id) == int(follower_id):
            return {"error": "User can't follow themselves"}, 400

        user = db.session.get(User, followed_id)
        if not user:
            return {"error": "User not found"}, 404

        exists = db.session.execute(
            db.select(follows).where(
                follows.c.followed_id == followed_id,
                follows.c.follower_id == follower_id
            )
        ).first()

        if exists:
            # Unfollow it
            db.session.execute(
                follows.delete().where(
                    follows.c.followed_id == followed_id,
                    follows.c.follower_id == follower_id
                )
            )
            db.session.commit()
            return {"message": "User unfollowed successfully"}, 200

        db.session.execute(
            follows.insert().values(followed_id=followed_id, follower_id=follower_id)
        )
        db.session.commit()
        return {"message": "User followed successfully"}, 200


    @staticmethod
    def get_image(image_name):
        # needs absolute path. doesnt find the folder otherwise
        dir_path = os.path.abspath(current_app.config["UPLOAD_FOLDER"])

        return send_from_directory(dir_path, image_name), 200
    
    @staticmethod
    def save_fcm(user_id, fcm_token):
        user = db.session.get(User, user_id)
        if not user:
            return {"error": "User not found"}, 404

        user.fcm_token = fcm_token
        db.session.commit()

        return {"message": "FCM token saved successfully"}, 200