from app.extensions import db

class Like(db.Model):
    __tablename__ = "likes"

    id :int = db.Column(db.Integer, primary_key=True)
    
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    user_id :int = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    post_id :int = db.Column(db.Integer, db.ForeignKey("posts.id"), nullable=False)

    def __repr__(self):
        return f"<Like {self.user_id}, {self.post_id}>"
