from sqlalchemy.orm import Session

from src.domain.repositories.task_interface import ITask
from src.models.task_model import Task as TaskModel
from src.schemas.task_schema import TaskCreateSchema, TaskResponseSchema


class SQLAlchemyTaskRepository(ITask):
    def __init__(self, db: Session):
        self.db = db

    def create(self, data: TaskCreateSchema) -> TaskResponseSchema:
        stmt = TaskModel(**data.model_dump())

        self.db.add(stmt)
        self.db.commit()
        self.db.refresh(stmt)

        return stmt

    def delete(self, id: int):
        pass

    def get_by_id(self, id: int):
        pass

    def update(self, data: TaskCreateSchema):
        pass
