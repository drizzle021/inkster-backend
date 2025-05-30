from app.extensions import db
from enum import Enum as PyEnum

# CREATE TYPE posttype AS ENUM ('Illustration', 'Novel', 'Manga');
# Needs Enum defined in database before use
class ReportType(PyEnum):
    HATE = "HATE"
    ABUSE = "ABUSE"
    VIOLENT = "VIOLENT"
    PRIVACY = "PRIVACY"
    SPAM = "SPAM"
    IMPERSONATION = "IMPERSONATION"

class Status(PyEnum):
    PENDING = "PENDING"
    ACCEPTED = "ACCEPTED"
    DENIED = "DENIED"



class Report(db.Model):
    __tablename__ = "reports"

    id :int = db.Column(db.Integer, primary_key=True)
    report_type: str = db.Column(db.Enum(ReportType), nullable=False)
    description :str = db.Column(db.String(300), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    status: str = db.Column(db.Enum(Status), nullable=False)


    author_id :int = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    post_id :int = db.Column(db.Integer, db.ForeignKey("posts.id", ondelete="CASCADE"), nullable=False)

    author = db.relationship("User", back_populates="reports")
    post = db.relationship("Post", back_populates="reports")


    def __repr__(self):
        return f"<Report {self.author_id}, #{self.id}>"
