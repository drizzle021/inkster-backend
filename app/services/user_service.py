from app.models import User, Post, Tag
from app.extensions import db
from werkzeug.utils import secure_filename
import os
from app.models.user import follows, saved_posts
from app.utils import endcode_filename, validate_filename
from flask import current_app

class UserService:
    @staticmethod
    def get_all_users():
        """
        Retrieves all users from the database.
        """
        users = User.query.all()
        return [
            {
                "id": user.id,
                "username": user.username,
                "email": user.email,
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
        
        return {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "profile_picture": user.profile_picture,
            "banner": user.banner,
            "tags": [tag.name for tag in user.tags],
            "posts": [
                {
                    "id": post.id,
                    "title": post.title,
                    "post_type": post.post_type.name,
                    "caption": post.caption,
                    "description": post.description,
                    "is_spoilered": post.is_spoilered,
                    "software": post.software,
                    "created_at": post.created_at
                    
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
            encoded_filename = endcode_filename(profile_picture.filename)
            file_path = os.path.join(current_app.config["UPLOAD_FOLDER"], encoded_filename)
            profile_picture.save(file_path)
            
            user.profile_picture = encoded_filename 

        if banner:
            encoded_filename = endcode_filename(banner.filename)
            file_path = os.path.join(current_app.config["UPLOAD_FOLDER"], encoded_filename)
            banner.save(file_path)
            
            user.banner = encoded_filename 


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
                "caption": post.caption,
                "is_spoilered": post.is_spoilered,
                "description": post.description,
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
