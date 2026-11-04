import logging

from flask import jsonify
from pydantic import ValidationError
from sqlalchemy.orm import Session

from src.repositories.task_repository import TaskRepository
from src.repositories.user_repository import UserRepository
from src.schemas.task_schema import TaskCreateSchema, TaskResponseSchema

logger = logging.getLogger(__name__)


class TaskService:
    def __init__(self, db: Session):
        self.__db = db
        self.__repository = TaskRepository(db)

    def create_task(self, data: TaskCreateSchema):
        """Create a new task method

        Args:
            data (TaskCreateSchema): Task request body
        """
        try:
            task_data = TaskCreateSchema.model_validate(data)
        except ValidationError as exec:
            logger.error(
                f"POST /v1/tasks rejeitado: Dados inválidos.\n details :{exec.errors(include_url=False)}"
            )
            return jsonify(
                {"error": "Dados inválidos", "details": exec.errors(include_url=False)}
            )

        user_repository = UserRepository(self.__db)

        if not user_repository.get_user_by_id(task_data.user_id):
            logger.error(
                "POST /v1/tasks rejeitado: Dados inválidos.\n details : usuário não existe"
            )
            return jsonify({"error": "Dados inválidos", "details": "Usuário inválido"})

        stmt = self.__repository.create(task_data)

        return TaskResponseSchema.model_validate(stmt)
