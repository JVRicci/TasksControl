from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from src.models.task_model import Task
from src.schemas.task_schema import TaskCreateSchema, TaskUpdateSchema


class TaskRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, data: TaskCreateSchema) -> Task:
        task = Task(**data.model_dump())
        self.db.add(task)

        self.db.commit()
        self.db.refresh(task)
        return task

    def delete(self, id: int) -> bool:
        stmt = delete(Task).where(Task.id == id)
        result = self.db.execute(stmt)
        self.db.commit()

        return result.rowcount > 0

    def get_by_id(self, id: int) -> Task | None:
        query = select(Task).where(Task.id == id)
        return self.db.execute(query).scalar_one_or_none()

    def get_by_user(self, user_id: int) -> list[Task]:
        query = select(Task).where(Task.user_id == user_id)
        return self.db.execute(query).scalars().all()

    def get_by_status(self, user_id: int, status: bool):
        query = select(Task).where(Task.user_id == user_id, Task.completed == status)
        return self.db.execute(query).scalars().all()

    def update(self, data: TaskUpdateSchema) -> Task | None:
        query = select(Task).where(Task.id == data.id).with_for_update()
        task = self.db.execute(query).scalar_one_or_none()

        if task is None:
            return None

        task.title = data.title if data.title else task.title
        task.description = data.description if data.description else task.description
        task.completed = data.completed if data.completed else task.completed

        self.db.commit()
        self.db.refresh(task)
        return task
