from app.models import User
from app.extensions import db
from flask_jwt_extended import create_access_token
import bcrypt
from app.models.user import Role

class AuthService:
    @staticmethod
    def register_user(username, email, password):
        """
        Creates a new user in the database.

        Args:

            data (dict): Contains "username", "email", "password".
        """


        # Check if username or email already exists
        if User.query.filter((User.username == username) | (User.email == email)).first():
            return {"error": "Username or email already exists"}, 409
        
        hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
        user = User(
            username=username,
            email=email,
            password=hash,
            role=Role.ARTIST,
            profile_picture="", # static image after registration
            banner="" # static image registration
        )
        db.session.add(user)
        db.session.commit()

        return {"message": "New user added successfully"}, 201
    
    @staticmethod
    def authenticate_user(email, password):
        """
        Authenticate a user and generate an access token.

        Args:
        
            data (dict): Contains "email" and "password".
        """
        user = User.query.filter_by(email=email).first()
        if not user:
            return {"error": "Invalid email or password"}, 401

        # Verify the password
        if not bcrypt.checkpw(password.encode("utf-8"), user.password.encode("utf-8")):
            return {"error": "Invalid email or password"}, 401

        # Generate token
        # use additional claims for more details -> create_access_token(identity=str(user.id), additional_claims={"username": user.username} )
        access_token = create_access_token(identity=str(user.id))
        return {"access_token": access_token}, 200