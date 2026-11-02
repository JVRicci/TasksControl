from flask import Blueprint, jsonify

api_bp = Blueprint("health_check", __name__)


@api_bp.route("/", methods=["GET"])
def health_check():
    response = {"status": "healthy"}
    return jsonify(response)
