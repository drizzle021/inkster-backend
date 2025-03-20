from app.extensions import db

class User(db.Model):
    __tablename__ = "users"

    id :int = db.Column(db.Integer, primary_key=True)
    username :str = db.Column(db.String(50), nullable=False, unique=True)
    email :str = db.Column(db.String(100), nullable=False, unique=True)
    password :str = db.Column(db.String(255), nullable=False)
    # role :str =
    profile_picture :str = db.Column(db.String(100), nullable=False)
    banner :str = db.Column(db.String(100), nullable=False)
    #date_joined =

    posts = db.relationship("Post", backref="author", lazy=True)

    def __repr__(self):
        return f"<User {self.username}>"



user_tags = db.Table(
    "user_tags",
    db.Column("user_id", db.Integer, db.ForeignKey("users.id"), primary_key=True),
    db.Column("tag_id", db.Integer, db.ForeignKey("tags.id"), primary_key=True)
)

follows = db.Table(
    "follows",
    db.Column("follower_id", db.Integer, db.ForeignKey("users.id"), primary_key=True),
    db.Column("followed_id", db.Integer, db.ForeignKey("users.id"), primary_key=True),
    db.Column("followed_at", db.DateTime, server_default=db.func.now())
)