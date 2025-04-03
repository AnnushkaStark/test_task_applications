from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from models import User
from schemas.user import UserBase, UserCreate

from .async_crud import BaseAsyncCRUD


class UserCRUD(BaseAsyncCRUD[User, UserBase, UserCreate]):
    async def get_by_username(
        self, db: AsyncSession, username: str
    ) -> Optional[User]:
        statement = select(self.model).where(self.model.username == username)
        result = await db.execute(statement)
        return result.scalars().first()

    async def get_by_email(
        self, db: AsyncSession, email: str
    ) -> Optional[User]:
        statement = select(self.model).where(self.model.email == email)
        result = await db.execute(statement)
        return result.scalars().first()

    async def get_by_id(self, db: AsyncSession, obj_id: int) -> Optional[User]:
        statement = (
            select(self.model)
            .options(joinedload(self.model.verify_code))
            .where(self.model.id == obj_id)
        )
        result = await db.execute(statement)
        return result.scalars().unique().first()

    async def mark_verify(self, db: AsyncSession, db_obj_id: int) -> User:
        user = await self.get_by_id(db=db, obj_id=db_obj_id)
        if user:
            user.is_verify = True
            await db.commit()
            await db.refresh(user)
            return user


user_crud = UserCRUD(User)
