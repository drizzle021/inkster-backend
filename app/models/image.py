from app.extensions import db

class Image(db.Model):
    __tablename__ = "images"

    id = db.Column(db.Integer, primary_key=True)
    image_name = db.Column(db.String(300), nullable=False)
    position = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    post_id = db.Column(db.Integer, db.ForeignKey("posts.id", ondelete="CASCADE"), nullable=False)

    post = db.relationship("Post", back_populates="images")

    def __repr__(self):
        return f"<Image {self.post_id}, {self.image_name}>"
