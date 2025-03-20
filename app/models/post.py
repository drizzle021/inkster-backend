from app.extensions import db

class Post(db.Model):
    __tablename__ = "posts"

    id :int = db.Column(db.Integer, primary_key=True)
    title :str = db.Column(db.String(100), nullable=False)
    # type :str = 
    caption :str = db.Column(db.String(3000), nullable=False)
    description :str = db.Column(db.String(300), nullable=True)
    is_spoilered :bool = db.Column(db.Boolean, nullable=False)
    software :str = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    # updated_at

    author_id :int = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    def __repr__(self):
        return f"<Post {self.title}>"


post_tags = db.Table(
    "post_tags",
    db.Column("post_id", db.Integer, db.ForeignKey("posts.id"), primary_key=True),
    db.Column("tag_id", db.Integer, db.ForeignKey("tags.id"), primary_key=True)
)