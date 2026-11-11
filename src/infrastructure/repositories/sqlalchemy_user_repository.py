from sqlalchemy import select
from sqlalchemy.orm import Session

from src.domain.repositories.user_interface import IUser
from src.models.user_model import User
from src.schemas.user_schema import UserCreateSchema, UserResponseSchema


class SQLAlchemyUserRepository(IUser):
    def __init__(self, db: Session):
        self.db = db

    def create(self, data: UserCreateSchema) -> UserResponseSchema:
        stmt = User(**data.model_dump())

        self.db.add(stmt)
        self.db.commit()
        self.db.refresh(stmt)

        return stmt

    def get_by_id(self, id: int) -> User | None:
        query = select(User).where(User.id == id)
        return self.db.execute(query).scalar_one_or_none()

    def get_by_email(self, email: str) -> User:
        query = select(User).find_by(User.email == email)
        return self.db.execute(query).scalar_one_or_none()

    def delete(self, id: int):
        pass

    def update(self, data: UserCreateSchema):
        pass
