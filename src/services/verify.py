from sqlalchemy.ext.asyncio import AsyncSession

from crud.verify import verification_code_crud
from schemas.verify import VerificationCodeCreate, VerificationCodeCreateDB


async def create(
    db: AsyncSession, create_schema: VerificationCodeCreate, user_id: int
) -> None:
    create_data = VerificationCodeCreateDB(
        **create_schema.model_dump(), user_id=user_id
    )
    await verification_code_crud.create(db=db, create_schema=create_data)
