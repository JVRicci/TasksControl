import logging

from flask import Blueprint, jsonify, make_response, request
from pydantic import ValidationError

from src.db.database import SessionLocal
from src.services.user_services import UserService

logger = logging.getLogger(__name__)

api_bp = Blueprint("users", __name__, url_prefix="/users")


@api_bp.route("", methods=["POST"])
def create_user():
    data = request.get_json(silent=True)

    try:
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

    except ValidationError as exc:
        logger.warning(f"POST /v1/users rejected: Dados inválidos. Detalhes:{exc}")

        return make_response(
            jsonify(
                {
                    "error": "Dados inválidos",
                    "details": exc.errors(include_url=False),
                }
            ),
            400,
        )

    except ValueError as exc:
        logger.warning(
            "POST /v1/users rejected: Erro ao cadastrar usuário. \nDetalhes: {exc}"
        )

        return make_response(
            jsonify({"error": str(exc)}),
            404,
        )


@api_bp.route("/<int:user_id>", methods=["GET"])
def get_user(user_id: int):
    try:
        with SessionLocal() as db:
            user_service = UserService(db)

            user = user_service.get_user_by_id(user_id)

            response = jsonify(user.model_dump(mode="json"))
            return make_response(response, 200)

    except ValueError as exc:
        logger.warning(
            "GET /v1/users rejected: Erro ao buscar usuário. Dados inválidos. \nDetalhes: {exc}"
        )

        return make_response(
            jsonify({"error": str(exc)}),
            404,
        )


@api_bp.route("/<string:user_email>", methods=["GET"])
def get_user_by_email(user_email):
    try:
        with SessionLocal() as db:
            user_service = UserService(db)

            user = user_service.get_user_by_email(user_email)

            response = jsonify(user.model_dump(mode="json"))

            return make_response(response, 200)

    except ValueError as exc:
        logger.warning(
            "GET /v1/users rejected: Erro ao buscar usuário. Dados inválidos. \nDetalhes: {exc}"
        )

        return make_response(
            jsonify({"error": str(exc)}),
            404,
        )


@api_bp.route("/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    try:
        with SessionLocal() as db:
            user_service = UserService(db)

            user_service.delete_user(user_id)

        return make_response("", 204)

    except ValueError as exc:
        logger.warning(
            "DELETE /v1/users rejected: Erro ao deletar usuário. Dados inválidos. \nDetalhes: {exc}"
        )

        return make_response(
            jsonify({"error": str(exc)}),
            404,
        )


@api_bp.route("", methods=["PATCH"])
def update_user():
    try:
        data = request.get_json(silent=True)
        with SessionLocal() as db:
            user_service = UserService(db)

            user = user_service.update_user(data)

        return make_response(jsonify(user.model_dump()), 200)

    except ValidationError as exc:
        logger.warning(
            "PATCH /v1/users rejected: Erro ao atualizar usuário. \nDetalhes: {exc}"
        )

        return make_response(
            jsonify(
                {
                    "error": "Parâmetros inválidos",
                    "details": exc.errors(include_url=False),
                }
            ),
            400,
        )

    except ValueError as exc:
        logger.warning(
            "PATCH /v1/users rejected: Erro ao atualizar usuário. Dados inválidos. \nDetalhes: {exc}"
        )

        return make_response(
            jsonify({"error": str(exc)}),
            404,
        )
