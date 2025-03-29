from flask import Blueprint, request, jsonify
from app.services.report_service import ReportService

report_bp = Blueprint("reports", __name__)

@report_bp.route("/reports", methods=["GET"])
def get_reports():
    """
    Route to retrieve all reports.
    """

    response, status_code = ReportService.get_all_reports()
    
    return jsonify(response), status_code


@report_bp.route("/reports/<int:id>", methods=["GET"])
def get_report(id):
    """
    Route to retrieve a report with a specific ID.
    """

    response, status_code = ReportService.get_report(id)

    return jsonify(response), status_code


@report_bp.route("/reports/<int:id>", methods=["POST"])
def resolve_report(id):
    """
    Route to mark report as resolved after reviewal
    """
    pass