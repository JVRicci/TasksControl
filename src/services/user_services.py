import logging

from flask import jsonify
from pydantic import ValidationError
from sqlalchemy.orm import Session

from src.repositories.user_repository import UserRepository
from src.schemas.user_schema import UserCreateSchema, UserResponseSchema

logger = logging.getLogger(__name__)


class UserService:
    def __init__(self, db: Session):
        self.__repository = UserRepository(db)

    def create_user(self, data: UserCreateSchema) -> UserResponseSchema:
        """Create a new user with data

        Args:
            data (UserCreateSchema): User arguments

        Returns:
            UserResponseSchema: User object
        """
        try:
            user_data = UserCreateSchema.model_validate(data)
        except ValidationError as exc:
            logger.error(
                f"POST /v1/users rejeitado: Dados inválidos.\n details :{exc.errors(include_url=False)}"
            )
            return jsonify(
                {"error": "Dados inválidos", "details": exc.errors(include_url=False)}
            )

        stmt = self.__repository.create_user(user_data)

        return UserResponseSchema.model_validate(stmt)

    def get_user_by_id(self, id: int) -> UserResponseSchema:
        stmt = self.__repository.get_user_by_id(id)

        return UserResponseSchema.model_validate(stmt)
