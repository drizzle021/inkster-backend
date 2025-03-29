from app.extensions import db

class Image(db.Model):
    __tablename__ = "images"

    id :int = db.Column(db.Integer, primary_key=True)
    
    image_name :str = db.Column(db.String(300), nullable=False)
    position :int = db.Column(db.Integer, primary_key=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    post_id :int = db.Column(db.Integer, db.ForeignKey("posts.id"), nullable=False)

    def __repr__(self):
        return f"<Image {self.post_id}, {self.image_name}>"
