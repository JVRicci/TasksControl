import logging

from flask import Blueprint, jsonify, make_response, request

from src.db.database import SessionLocal
from src.services.user_services import UserService

logger = logging.getLogger(__name__)

api_bp = Blueprint("users", __name__, url_prefix="/users")


@api_bp.route("", methods=["POST"])
def create_user():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        logger.warning("POST /v1/users rejeitado: corpo JSON ausente ou inválido")
        return make_response(
            jsonify({"error": "Envie um objeto JSON válido"}),
            400,
        )

    with SessionLocal() as db:
        user_service = UserService(db)

        user = user_service.create_user(data)

        response = jsonify(user.model_dump(mode="json"))
        return make_response(response, 201)


@api_bp.route("/<int:user_id>", methods=["GET"])
def get_user(user_id: int):
    with SessionLocal() as db:
        user_service = UserService(db)

        user = user_service.get_user_by_id(user_id)

        response = jsonify(user.model_dump(mode="json"))
        return make_response(response, 200)
