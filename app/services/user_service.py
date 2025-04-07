from app.models import User, Post
from app.extensions import db
from werkzeug.utils import secure_filename
import os
from app.models.user import follows, saved_posts

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
            # "posts": user.posts,

        }, 200
        

    @staticmethod
    def update_pictures(files):
        """
        Updates the user's profile picture or banner

        Args:
        
            files (dict): 
        """
        user = db.session.get(User, id)
        if not user:
            return {"error": "User not found"}, 404
        
        if "profile_picture" in files:
            file = files["profile_picture"]

            # if allowed_file(file.filename):
            #     filename = secure_filename(file.filename)
            #     filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            #     file.save(filepath)
            #     user.profile_picture = filepath  # Save the file path to the 
            
            filename = secure_filename(file.filename)
            filepath = os.path.join("./static/uploads", filename)
            file.save(filepath)
            user.profile_picture = filepath 

        # same for banner
        # .
        # .


        db.session.commit()
        return {"message": "Profile updated successfully"}, 200

    @staticmethod
    def get_saved_posts(user_id):
        posts = db.session.execute(
            db.select(Post).join(saved_posts).where(saved_posts.c.user_id == user_id)
        ).scalars().all()

        return [
            {
                "id": post.id,
                "title": post.title,
                "caption": post.caption,
                "author_id": post.author_id
            }
            for post in posts
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
