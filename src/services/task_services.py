import logging

from sqlalchemy.orm import Session

from src.infrastructure.repositories.sqlalchemy_task_repository import (
    SQLAlchemyTaskRepository,
)
from src.infrastructure.repositories.sqlalchemy_user_repository import (
    SQLAlchemyUserRepository,
)
from src.schemas.task_schema import TaskCreateSchema, TaskResponseSchema

logger = logging.getLogger(__name__)


class TaskService:
    def __init__(self, db: Session):
        self.db = db
        self.repository = SQLAlchemyTaskRepository(db)

    def create_task(self, data: TaskCreateSchema):
        """Create a new task method

        Args:
            data (TaskCreateSchema): Task request body
        """
        task_data = TaskCreateSchema.model_validate(data)

        user_repository = SQLAlchemyUserRepository(self.db)

        if not user_repository.get_by_id(task_data.user_id):
            raise ValueError("Usuário inválido")

        stmt = self.repository.create(task_data)

        return TaskResponseSchema.model_validate(stmt)
