from app.models import User
from app.extensions import db

def create_user(data):
    """
    Creates a new user in the database.
    """
    # Check if username or email already exists
    if User.query.filter((User.username == data["username"]) | (User.email == data["email"])).first():
        return {"error": "Username or email already exists"}, 409

    # Create and save new user
    new_user = User(
        username=data["username"],
        email=data["email"],
        password=data["password"],  # TODO: hash password
        profile_picture=data["profile_picture"],
        banner=data["banner"]
    )
    db.session.add(new_user)
    db.session.commit()
    return {"message": "User created successfully"}, 201


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
            "profile_picture": user.profile_picture,
            "banner": user.banner
        }
        for user in users
    ]
