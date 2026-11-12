from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, validates

from src.db.base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)

    @validates("email")
    def validate_email(self, key, address):
        if "@" not in address:
            raise ValueError("Invalid email adress")
        return address.lower()
