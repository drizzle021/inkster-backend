from app.models import Report
from app.extensions import db

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
            }
            for report in reports
        ]
    
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

        }, 200
