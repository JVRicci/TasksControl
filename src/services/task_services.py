import logging

from sqlalchemy.orm import Session

from src.infrastructure.repositories.sqlalchemy_task_repository import (
    SQLAlchemyTaskRepository,
)
from src.infrastructure.repositories.sqlalchemy_user_repository import (
    SQLAlchemyUserRepository,
)
from src.schemas.task_schema import (
    TaskCreateSchema,
    TaskResponseSchema,
    TaskUpdateSchema,
)

logger = logging.getLogger(__name__)


class TaskService:
    def __init__(self, db: Session):
        self.db = db
        self.repository = SQLAlchemyTaskRepository(db)

    def create_task(self, data: TaskCreateSchema) -> TaskResponseSchema:
        """Create a new task method

        Args:
            data (TaskCreateSchema): Task request body
        """
        task_data = TaskCreateSchema.model_validate(data)

        user_repository = SQLAlchemyUserRepository(self.db)

        if not user_repository.get_by_id(task_data.user_id):
            logger.warning("Não foi possivel criar tarefa. Usuário inválido.")
            raise ValueError("Usuário inválido")

        stmt = self.repository.create(task_data)

        return TaskResponseSchema.model_validate(stmt)

    def get_task_by_id(self, task_id: int) -> TaskResponseSchema:
        """Retorna uma tarefa com base no ID dela

        Args:
            task_id (int): _description_

        Returns:
            TaskResponseSchema: _description_
        """
        stmt = self.repository.get_by_id(task_id)

        if stmt is None:
            raise ValueError("Tarefa não encontrada")

        return TaskResponseSchema.model_validate(stmt)

    def get_by_user(self, user_id: int) -> list[TaskResponseSchema]:
        """Retorna uma lista de tarefas com base no id de um usuário

        Args:
            user_id (int): _description_

        Raises:
            ValueError: _description_

        Returns:
            list[TaskResponseSchema]: _description_
        """
        user_repository = SQLAlchemyUserRepository(self.db)

        if not user_repository.get_by_id(user_id):
            logger.warning("Não foi possível obter tarefa. Usuário inválido")
            raise ValueError("Usuário inválido")

        task_list = self.repository.get_by_user(user_id)

        return [TaskResponseSchema.model_validate(task) for task in task_list]

    def get_by_status(self, user_id: int, status: bool) -> list[TaskResponseSchema]:
        """Retorna uma lista de tarefas com base no id do Usuário e se estão ocmpletas ou não

        Args:
            user_id (int): _description_
            status (bool): _description_

        Raises:
            ValueError: _description_

        Returns:
            list[TaskResponseSchema]: _description_
        """
        user_repository = SQLAlchemyUserRepository(self.db)

        if not user_repository.get_by_id(user_id):
            logger.warning("Não foi possível obter tarefa. Usuário inválido")
            raise ValueError("Usuário inválido")

        task_list = self.repository.get_by_status(user_id, status)

        return [TaskResponseSchema.model_validate(task) for task in task_list]

    def update_task(self, data: TaskUpdateSchema) -> TaskResponseSchema:
        """Atualiza dados de uma tarefa

        Args:
            data (TaskUpdateSchema): _description_

        Returns:
            TaskResponseSchema: _description_
        """
        update_values = TaskUpdateSchema(data)

        stmt = self.repository.update(data.id, update_values)

        return stmt
