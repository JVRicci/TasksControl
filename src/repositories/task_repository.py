from sqlalchemy.orm import Session

from src.models.task_model import Task as TaskModel
from src.schemas.task_schema import TaskCreateSchema, TaskResponseSchema


class TaskRepository:
    def __init__(self, db: Session):
        self.__db = db

    def create(self, data: TaskCreateSchema) -> TaskResponseSchema:
        stmt = TaskModel(**data.model_dump())

        self.__db.add(stmt)
        self.__db.commit()
        self.__db.refresh(stmt)

        return stmt
