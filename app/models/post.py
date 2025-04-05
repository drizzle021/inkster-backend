from app.extensions import db
from enum import Enum as PyEnum

# CREATE TYPE posttype AS ENUM ('Illustration', 'Novel', 'Manga');
# Needs Enum defined in database before use
class PostType(PyEnum):
    ILLUSTRATION = "ILLUSTRATION"
    NOVEL = "NOVEL"
    MANGA = "MANGA"

class Post(db.Model):
    """
    Represents a post in the system.

    Attributes:
        id (int): Identifier number of the user.
        title (str): The title chosen by the user.
        post_type (str): The type of the post (Illustration/Manga/Novel).
        caption (str): The caption of the post.
        description (str): Decription of the post.
        is_spoilered (bool): Condition if the post is spoilered.
        software (str): The software the post was created in.
        created_at : Creation date of the post.
    """
        
    __tablename__ = "posts"

    id :int = db.Column(db.Integer, primary_key=True)
    title :str = db.Column(db.String(100), nullable=False)
    post_type :str = db.Column(db.Enum(PostType), nullable=False)
    caption :str = db.Column(db.String(3000), nullable=False)
    description :str = db.Column(db.String(300), nullable=True)
    is_spoilered :bool = db.Column(db.Boolean, nullable=False)
    software :str = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    # updated_at

    author_id :int = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    # TODO: lazy load images (?)


    def __repr__(self):
        return f"<Post {self.title}>"


post_tags = db.Table(
    "post_tags",
    db.Column("post_id", db.Integer, db.ForeignKey("posts.id"), primary_key=True),
    db.Column("tag_id", db.Integer, db.ForeignKey("tags.id"), primary_key=True)
)