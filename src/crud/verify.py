from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import VerificationCode
from schemas.verify import VerificationCodeBase, VerificationCodeCreate

from .async_crud import BaseAsyncCRUD


class VerificationCodeCRUD(
    BaseAsyncCRUD[
        VerificationCode, VerificationCodeCreate, VerificationCodeBase
    ]
):
    async def get_by_user_id(
        self, db: AsyncSession, user_id: int
    ) -> Optional[VerificationCode]:
        statement = select(self.model).where(self.model.user_id == user_id)
        result = await db.execute(statement)
        return result.scalars().first()


verification_code_crud = VerificationCodeCRUD(VerificationCode)
