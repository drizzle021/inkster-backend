from flask import Blueprint, request, jsonify
from app.services.map_service import MapService

map_bp = Blueprint("map", __name__)

@map_bp.route("/map/nearby-exhibitions", methods=["GET"])
def get_nearby_exhibitions():
    """
    Get nearby exhibitions (galleries, museums, etc.) using Google Places API.
    Required: lat, lng
    Optional: radius (default: 5000m)
    """
    lat = request.args.get("lat")
    lng = request.args.get("lng")
    radius = request.args.get("radius", 5000)

    if not lat or not lng:
        return jsonify({"error": "Missing latitude or longitude"}), 400

    response, status_code = MapService.get_nearby_exhibitions(lat, lng, radius)
    return jsonify(response), status_code
