from sqlalchemy import delete, select, update
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session, selectinload

from src.domain.repositories.task_interface import ITask
from src.models.task_model import Task
from src.schemas.task_schema import TaskCreateSchema, TaskResponseSchema


class SQLAlchemyTaskRepository(ITask):
    def __init__(self, db: Session):
        self.db = db

    def create(self, data: TaskCreateSchema) -> dict:
        stmt = Task(**data.model_dump())

        self.db.add(stmt)
        self.db.commit()
        self.db.refresh(stmt)

        return stmt

    def delete(self, id: int) -> dict:
        try:
            user = self.db.execute(select(Task).where(Task.id == id)).scalar_one()
            stmt = self.db.delete(user)
            self.db.commit()

            return stmt

        except NoResultFound:
            self.db.rollback()

            return {"erro": "Usuário não encontrado"}

    def get_by_id(self, id: int) -> list[dict] | dict:
        query = select(Task).where(Task.id == id).limit(1)

        return self.db.execute(query).scalar()

    def get_by_user(self, user_id: int) -> list[dict]:
        try:
            query = select(Task).where(Task.user_id == user_id)
            return list(self.db.execute(query).scalars().all())

        except NoResultFound:
            self.db.rollback()
            return {"erro": "Nenhum registro encontrado"}

    def update(self, data: TaskCreateSchema, user_id: int) -> dict | None:
        try:
            query = select(Task).where(Task.id == user_id).with_for_update()
            task = self.db.execute(query).scalar_one_or_none()

            if task is None:
                return None

            task.title = data.title
            task.description = data.description
            task.completed = data.completed

            self.db.flush()
            return task

        except NoResultFound:
            self.db.rollback()

            return {"erro": "Usuário não encontrado"}
