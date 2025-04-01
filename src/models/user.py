import uuid
from typing import TYPE_CHECKING, List

from sqlalchemy import UUID, Boolean, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from databases.database import Base

if TYPE_CHECKING:
    from .application import Application


class User(Base):
    """
    Модель пользователя

    ## Attrs:
        - id: int - идентификатор
        - uid: UUID - идентификатор
        - username: str - юзернейм
        - email: str - электронная почта
        - passowrd: str - хэш пароля
        - is_verify: bool - пользователь верифицирован или нет
        - applications: List[application] - заявки пользователя
    """

    __tablename__ = "user"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    uid: Mapped[uuid.UUID] = mapped_column(
        UUID, unique=True, index=True, default=uuid.uuid4
    )
    username: Mapped[str]
    email: Mapped[str]
    password: Mapped[str]
    is_verify: Mapped[bool] = mapped_column(Boolean, default=False)
    applications: Mapped[List["Application"]] = relationship(
        "Application", back_populates="author"
    )
