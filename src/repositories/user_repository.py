from sqlalchemy import delete, select, update
from sqlalchemy.orm import Session

from src.models.user_model import User
from src.repositories.contract.repository_interface import IRepository
from src.schemas.user_schema import UserCreateSchema, UserResponseSchema


class UserRepository(IRepository):
    def __init__(self, db: Session):
        self.db = db

    def create(self, data: UserCreateSchema) -> UserResponseSchema:
        stmt = User(**data.model_dump())
        self.db.add(stmt)
        self.db.flush()
        self.db.refresh(stmt)
        return stmt

    def get_by_id(self, id: int) -> User | None:
        query = select(User).where(User.id == id)
        return self.db.execute(query).scalar_one_or_none()

    def get_by_email(self, email: str) -> User:
        query = select(User).find_by(User.email == email)
        return self.db.execute(query).scalar_one_or_none()

    def delete(self, id: int) -> bool:
        query = delete(User).where(User.id == id)

        result = self.db.execute(query)
        self.db.commit()

        return result.rowcount > 0

    def update(self, data: UserCreateSchema) -> User | None:
        query = select(User).where(User.id == data.id).with_for_update()
        user = self.db.execute(query).scalar_one_or_none()

        if user is None:
            return None

        user.name = data.name if data.name else user.name
        user.email = data.email if data.email else user.email
        user.password = data.password if data.password else user.password

        self.db.commit()
        self.db.refresh(User)

        return user
