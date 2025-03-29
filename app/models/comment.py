from app.extensions import db

class Comment(db.Model):
    __tablename__ = "comments"

    id :int = db.Column(db.Integer, primary_key=True)
    
    content :str = db.Column(db.String(300), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    author_id :int = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    post_id :int = db.Column(db.Integer, db.ForeignKey("posts.id"), nullable=False)

    def __repr__(self):
        return f"<Comment {self.author_id}, {self.content}>"
