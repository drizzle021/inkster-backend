from app.models import User
from app.extensions import db
from werkzeug.utils import secure_filename
import os

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
        ]
    
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
