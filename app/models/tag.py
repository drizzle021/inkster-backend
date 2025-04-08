from app.extensions import db

class Tag(db.Model):
    __tablename__ = "tags"

    id :int = db.Column(db.Integer, primary_key=True)
    name :str = db.Column(db.String(50), nullable=False, unique=True)
   
    posts = db.relationship(
        "Post",
        secondary="post_tags",
        back_populates="tags",
        passive_deletes=True
    )

    users = db.relationship(
        "User",
        secondary="user_tags",
        back_populates="tags",
        passive_deletes=True
    )


    def __repr__(self):
        return f"<Tag {self.name}>"
