from flask import Blueprint, request, jsonify
from app.services.report_service import ReportService
from flask_jwt_extended import jwt_required, get_jwt_identity


report_bp = Blueprint("reports", __name__)

@report_bp.route("/reports", methods=["GET"])
@jwt_required()
def get_reports():
    """
    Route to retrieve all reports.
    """

    status = request.args.get("status")

    response, status_code = ReportService.get_all_reports(status)
    
    return jsonify(response), status_code


@report_bp.route("/reports/<int:id>", methods=["GET"])
@jwt_required()
def get_report(id):
    """
    Route to retrieve a report with a specific ID.
    """

    response, status_code = ReportService.get_report(id)

    return jsonify(response), status_code


@report_bp.route("/reports/ignore/<int:id>", methods=["POST"])
@jwt_required()
def ignore_report(id):
    """
    Route to mark report as resolved after reviewal
    """

    identity = get_jwt_identity()
    response, status_code = ReportService.ignore_report(id, identity)


    return jsonify(response), status_code


@report_bp.route("/reports/remove-post/<int:id>", methods=["POST"])
@jwt_required()
def remove_post(id):
    """
    Route to mark report as resolved after reviewal
    """
    identity = get_jwt_identity()
    response, status_code = ReportService.remove_post(id, identity)


    return jsonify(response), status_code