from app.extensions import db
from enum import Enum as PyEnum
import bcrypt

# CREATE TYPE role AS ENUM ('Artist', 'Moderator');
# Needs Enum defined in database before use
class Role(PyEnum):
    ARTIST = "ARTIST"
    MODERATOR = "MODERATOR"

class User(db.Model):
    """
    Represents a user in the system.

    Attributes:
        id (int): Identifier number of the user.
        username (str): The username chosen by the user.
        email (str): The user's e-mail address.
        password (str): Hashed password.
        role (str): Role of the user (Artist/Moderator).
        profile_picture (str): Path to the location of the user's uploaded profile picture.
        banner (str): Path to the location of the user's uploaded profile picture.
        date_joined : Registration date of the user.
    """

    __tablename__ = "users"

    id :int = db.Column(db.Integer, primary_key=True)
    username :str = db.Column(db.String(50), nullable=False, unique=True)
    email :str = db.Column(db.String(100), nullable=False, unique=True)
    password :str = db.Column(db.String(255), nullable=False)
    role :str = db.Column(db.Enum(Role), nullable=False)
    profile_picture :str = db.Column(db.String(100), nullable=False)
    banner :str = db.Column(db.String(100), nullable=False)
    date_joined = db.Column(db.DateTime, server_default=db.func.now())

    posts = db.relationship("Post", back_populates="author", lazy=True, cascade="all, delete-orphan", passive_deletes=True)
    likes = db.relationship("Like", back_populates="user", cascade="all, delete-orphan", passive_deletes=True)
    comments = db.relationship("Comment", back_populates="author", cascade="all, delete-orphan", passive_deletes=True)
    reports = db.relationship("Report", back_populates="author", cascade="all, delete-orphan", passive_deletes=True)
    saved_posts = db.relationship(
        "Post",
        secondary="saved_posts",
        back_populates="savers",
        lazy="dynamic",
        passive_deletes=True
    )
    tags = db.relationship(
        "Tag",
        secondary="user_tags",
        back_populates="users",
        passive_deletes=True
    )


    def __repr__(self):
        return f"<User {self.username} #{self.id}>"
    
user_tags = db.Table(
    "user_tags",
    db.Column("user_id", db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), primary_key=True),
    db.Column("tag_id", db.Integer, db.ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True)
)

follows = db.Table(
    "follows",
    db.Column("follower_id", db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), primary_key=True),
    db.Column("followed_id", db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), primary_key=True),
    db.Column("followed_at", db.DateTime, server_default=db.func.now())
)

saved_posts = db.Table(
    "saved_posts",
    db.Column("post_id", db.Integer, db.ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True),
    db.Column("user_id", db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), primary_key=True),
    db.Column("saved_at", db.DateTime, server_default=db.func.now())
)