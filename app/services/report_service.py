from app.models import Report, User, Post
from app.models.report import Status, ReportType
from app.models.user import Role
from app.extensions import db
from flask_jwt_extended import jwt_required, get_jwt_identity


class ReportService:
    @staticmethod
    # pagination here maybe
    def get_all_reports(status=None):
        """
        Retrieves all reports from the database.
        If a status is provided, filters reports by that status.
        """

        if status:
            # If status is passed as a string (like "PENDING"), convert to enum
            try:
                reports = Report.query.filter(Report.status == Status(status.upper())).all()
            except ValueError:
                return {"error": f"Invalid status: {status}"}, 400
        else:
            reports = Report.query.all()

        return [
            {
                "id": report.id,
                "post_id": report.post_id,
                "report_type": report.report_type.name,
                "status": report.status.name,
            }
            for report in reports
        ], 200
    
    @staticmethod
    def get_report(id):
        """
        Retrieves a specific report from the database.

        Args:
        
            id (int): ID of the report to be retrieved.
        """
        report = db.session.get(Report, id)
        if not report:
            return {"error": "Report not found"}, 404
        
        return {
            "id": report.id,
            "post_id": report.post_id,
            "report_type": report.report_type.name,
            "description": report.description,
            "post": {
                "title": report.post.title,
                "caption": report.post.caption,
                "description": report.post.description,
                "tags": [
                    t.name for t in report.post.tags
                ],
                "author": {
                    "id": report.post.author.id,
                    "username": report.post.author.username,
                    "profile_picture": report.post.author.profile_picture,
                    "date_joined": report.post.author.date_joined
                },

                "created_at": report.post.created_at
            }
        }, 200

    @staticmethod
    def add_report(id, report_type, description, identity):
        """
        Creates a report in the database.

        Args:
        
            id (int): ID of the report to be created.
        """

        post = db.session.get(Post, id)

        if not post:
            return {"error": "Post not found"}, 404

        report = Report (
            report_type= ReportType(report_type),
            description= description,
            status= Status.PENDING,
            author_id= identity,
            post_id= id
        )


        db.session.add(report)
        db.session.commit()

        return {"message": "New report created successfully"}, 201


    @staticmethod
    def ignore_report(id, identity):
        """
        Resolves a report in the database.

        Args:
        
            id (int): ID of the report to be created.
        """


        report = db.session.get(Report, id)
        if not report:
            return {"error": "Report not found"}, 404
        
        logged_in_user = db.session.get(User, identity)

        if logged_in_user.role.name != "MODERATOR":
            return {"error": "Unauthorized"}, 401

        report.status = Status.DENIED
        db.session.add(report)
        db.session.commit()

        return {"message": "Report ignored successfully"}, 200


    @staticmethod
    def remove_post(id, identity):
        """
        Resolves a report in the database.

        Args:
        
            id (int): ID of the report to be created.
        """

        report = db.session.get(Report, id)
        if not report:
            return {"error": "Report not found"}, 404
        
        logged_in_user = db.session.get(User, identity)

        if logged_in_user.role.name != "MODERATOR":
            return {"error": "Unauthorized"}, 401

        report.status = Status.ACCEPTED
        db.session.add(report)
        db.session.commit()

        post = db.session.get(Post, report.post_id)
        db.session.delete(post)
        db.session.commit()

        return {"message": "Report ignored successfully"}, 200