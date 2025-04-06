from app.models import Report
from app.models.report import Status, ReportType
from app.extensions import db
from flask_jwt_extended import jwt_required, get_jwt_identity


class ReportService:
    @staticmethod
    # pagination here maybe
    def get_all_reports():
        """
        Retrieves all reports from the database.
        """
        reports = Report.query.all()
        return [
            {
                "id": report.id,
                "post_id": report.post_id,
                "report_type": report.report_type.name
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
            "description": report.description
        }, 200

    @staticmethod
    def add_report(id, report_type, description, identity):
        """
        Creates a report in the database.

        Args:
        
            id (int): ID of the report to be created.
        """

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
