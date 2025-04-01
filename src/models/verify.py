import uuid
from typing import TYPE_CHECKING

from sqlalchemy import UUID, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from databases.database import Base

if TYPE_CHECKING:
    from .user import User


class VerificationCode(Base):
    """
    Модель кода верификации

    ## Attrs:
      - id: int - идентификатор
      - uid: UUID - идентификатор
      - verification_code: str - код верификации
      - user_id: int - идентификатор пользователя
        которому выслан код
      - user: User - связь с пользователем
    """

    __tablename__ = "verification_code"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    uid: Mapped[uuid.UUID] = mapped_column(
        UUID, unique=True, index=True, default=uuid.uuid4
    )
    verification_code: Mapped[str] = mapped_column(String, nullable=False)
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False
    )
    user: Mapped["User"] = relationship("User", back_populates="verify_code")
