from flask import jsonify
from sqlalchemy.orm import Session

from src.models.user_model import User
from src.schemas.user_schema import UserCreateSchema, UserResponseSchema


class UserRepository:
    def __init__(self, db: Session):
        self.__db = db

    def create_user(self, data: UserCreateSchema) -> UserResponseSchema:
        user_data = User(**data.model_dump())

        self.__db.add(user_data)
        self.__db.commit()
        self.__db.refresh(user_data)

        return user_data

    def get_user_by_id(self, id: int) -> UserResponseSchema | dict:
        with self.__db as session:
            stmt = session.get(User, id)

            if not stmt:
                return jsonify({"error": "usuário não encontrado"})

        return stmt
