import logging

from sqlalchemy.orm import Session
from werkzeug.security import check_password_hash

from src.repositories.auth_repository import AuthRepository
from src.schemas.auth_schema import AuthSchema
from src.schemas.user_schema import UserResponseSchema

logger = logging.getLogger(__name__)


class AuthService:
    def __init__(self, db: Session):
        self.db = db
        self.repository = AuthRepository(db)

    def auth(self, data: AuthSchema):
        data = AuthSchema.model_validate(data)

        auth_repository = AuthRepository(self.db)
        stmt = auth_repository.get_auth_by_email(data)

        return UserResponseSchema.model_validate(stmt)
