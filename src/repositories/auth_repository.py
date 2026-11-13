from sqlalchemy import select
from sqlalchemy.orm import Session
from werkzeug.security import check_password_hash

from src.models.user_model import User
from src.schemas.auth_schema import AuthSchema


class AuthRepository:
    def __init__(self, db: Session):
        self.db = Session()

    def get_auth_by_email(self, data: AuthSchema) -> bool:
        query = select(User).where(User.email == data.email)
        stmt = self.db.execute(query).scalar_one_or_none()

        if not stmt or not AuthRepository.pass_validation(stmt.password, data.password):
            return False

        return stmt

    @staticmethod
    def pass_validation(query_pass: str, data_pass: str) -> bool:
        return check_password_hash(query_pass, data_pass)
