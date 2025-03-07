import typing
import uuid
from datetime import datetime

from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column

from api.models import Base


class User(Base):
    __tablename__ = "user"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, index=True)

    email: Mapped[str] = mapped_column(String(2048), unique=True, index=True)
    password_hash: Mapped[str]

    timezone: Mapped[str]

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))

    def to_dict(self) -> dict[str, typing.Any]:
        return {
            "id": self.id,
            "email": self.email,
            "password_hash": self.password_hash,
            "timezone": self.timezone,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    def __repr__(self) -> str:
        return f"<User {self.email}>"
