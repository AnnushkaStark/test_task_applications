import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import UUID, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import Mapped, mapped_column, relationship

from constants.application import ApplicationStatus
from databases.database import Base

if TYPE_CHECKING:
    from .user import User


class Application(Base):
    """
    Модель заявки

    ## Attrs:
      - id: int - идентификатор
      - uid: UUID - идентификатор
      - name: str - название
      - description: str - описание
      - status: ApplicationStatus - статус заявки
      - author_id: int - идентификатор пользователя
       (автора заявки) FK User
      -  author: User - связь с пользователем
    """

    __tablename__ = "application"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    uid: Mapped[uuid.UUID] = mapped_column(
        UUID, unique=True, index=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(String, index=True)
    description: Mapped[str]
    status: Mapped[ApplicationStatus] = mapped_column(
        ENUM(ApplicationStatus, create_type=False),
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    author_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("user.id", ondelete="CASCADE")
    )
    author: Mapped["User"] = relationship(
        "User", back_populates="applications"
    )
