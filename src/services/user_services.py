import logging

from sqlalchemy.orm import Session

from src.infrastructure.repositories.sqlalchemy_user_repository import (
    SQLAlchemyUserRepository,
)
from src.schemas.user_schema import UserCreateSchema, UserResponseSchema

logger = logging.getLogger(__name__)


class UserService:
    def __init__(self, db: Session):
        self.db = db
        self.repository = SQLAlchemyUserRepository(db)

    def create_user(self, data: UserCreateSchema) -> UserResponseSchema | dict:
        """Create a new user with data

        Args:
            data (UserResponseSchema): User arguments

        Returns:
            UserResponseSchema: User object
        """
        user_data = UserCreateSchema.model_validate(data)

        stmt = self.repository.create(user_data)

        return UserResponseSchema.model_validate(stmt)

    def get_user_by_id(self, id: int) -> UserResponseSchema:
        stmt = self.repository.get_user_by_id(id)

        return UserResponseSchema.model_validate(stmt)
