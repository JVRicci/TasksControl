import logging

from sqlalchemy.orm import Session
from werkzeug.security import generate_password_hash

from src.repositories.task_repository import TaskRepository
from src.repositories.user_repository import UserRepository
from src.schemas.user_schema import (
    UserCreateSchema,
    UserResponseSchema,
    UserUpdateSchema,
)

logger = logging.getLogger(__name__)


class UserService:
    def __init__(self, db: Session):
        self.db = db
        self.repository = UserRepository(db)

    def create_user(self, data: UserCreateSchema) -> UserResponseSchema | dict:
        """Create a new user with data

        Args:
            data (UserResponseSchema): User arguments

        Returns:
            UserResponseSchema: User object
        """
        user_data = data.model_copy(
            update={"password": generate_password_hash(data.password)}
        )

        stmt = self.repository.create(user_data)

        return UserResponseSchema.model_validate(stmt)

    def get_user_by_id(self, id: int) -> UserResponseSchema:
        stmt = self.repository.get_user_by_id(id)

        return UserResponseSchema.model_validate(stmt)

    def get_user_by_email(self, email: str) -> UserResponseSchema:
        stmt = self.repository.get_by_email(email)

        return UserResponseSchema.model_validate(stmt)

    def delete_user(self, user_id: int) -> bool:
        task_repository = TaskRepository(self.db)
        if task_repository.get_by_user(user_id):
            logger.warning(
                "DELETE /v1/users rejected: Usuário possui tarefas pendentes"
            )
            raise ValueError("Usuário possui tarefas pendentes")

        stmt = self.repository.delete(user_id)

        return stmt

    def update_user(
        self, user_id: int, user_data: UserUpdateSchema
    ) -> UserResponseSchema:
        stmt = self.repository.update(user_id, user_data)

        return UserResponseSchema.model_validate(stmt)
