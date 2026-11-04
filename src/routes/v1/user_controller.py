import logging

from flask import jsonify, make_response, request
from flask.views import MethodView

from src.db.database import SessionLocal
from src.schemas.user_schema import UserCreateSchema, UserResponseSchema
from src.services.user_services import UserService

logger = logging.getLogger(__name__)


class UserController(MethodView):
    def __init__(self):
        self.__db = SessionLocal()

    def post(self):
        data = request.get_json(silent=True)

        if not isinstance(data, dict):
            logger.warning("POST /v1/users rejeitado: corpo JSON ausente ou inválido")
            response = jsonify({"error": "Envie um objeto JSON válido"})
            return make_response(response, 406)

        with self.__db as db:
            user_service = UserService(db)

            user = user_service.create_user(data)
            data = jsonify(user.model_dump(mode="json"))
            return make_response(data, 201)

    def get(self, user_id: int) -> UserResponseSchema:
        if not isinstance(user_id, int):
            logger.warning("GET /v1/users rejeitado: tipo do ID inválido")
            response = jsonify({"error": "ID inválido"})
            return make_response(response, 406)

        with self.__db as db:
            user_service = UserService(db)

            user = user_service.get_user_by_id(user_id)
            response = jsonify(user.model_dump(mode="json"))
            return make_response(response, 200)
