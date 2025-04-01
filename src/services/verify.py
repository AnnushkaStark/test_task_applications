from sqlalchemy.ext.asyncio import AsyncSession
from models import VerificationCode
from schemas.verify import VerificationCodeCreate, VerificationCodeCreateDB
from crud.verify import verification_code_crud


async def create(db: AsyncSession, create_schema: VerificationCodeCreate, user_id: int):
    create_data = VerificationCodeCreateDB(**create_schema.model_dump(), user_id=user_id)
    code = await verification_code_crud.create(db=db, create_schema=create_data)
    return code