import logging

from flask import Blueprint, jsonify, make_response, request
from flask.views import MethodView
from flask_jwt_extended import create_access_token
from pydantic import ValidationError

from src.db.database import SessionLocal
from src.services.auth_service import AuthService

logger = logging.getLogger(__name__)

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


class AuthController(MethodView):
    def __init__(self, session):
        self.session = SessionLocal()

    def post(self):
        data = request.get_json(silent=True)

        try:
            with self.session as session:
                user = AuthService(session).auth(data)

            token = create_access_token(identity=str(user.id))

            return make_response(
                jsonify({"access_token": token, "token_type": "Bearer"}), 200
            )

        except (ValidationError, ValueError) as exc:
            logger.warning(
                f"POST /v1/auth rejected: Falha ao autenticar. Detalhes:{exc}"
            )

            make_response("Falha ao autenticar", 401)
