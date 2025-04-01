from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from crud.user import user_crud
from services import verify as verification_service
from models import User
from schemas.user import UserCreate, UserLogin
from schemas.verify import VerificationCodeCreate
from utilities.email_client import email_client
from utilities.security.password_hasher import (
    get_password_hash,
    verify_password,
)
from utilities.security.security import TokenSubject, create_tokens
from utilities.verification import generate_veriify_code


async def create(db: AsyncSession, create_data: UserCreate) -> Optional[User]:
    if await user_crud.get_by_username(db=db, username=create_data.username):
        raise Exception("Username alredy exist")
    if await user_crud.get_by_email(db=db, email=create_data.email):
        raise Exception("Email alredy exist")
    create_data.password = get_password_hash(create_data.password)
    user = await user_crud.create(
        db=db, create_schema=create_data.model_dump()
    )
    verify_code = await generate_veriify_code()
    verification_code_schema = VerificationCodeCreate(verification_code=verify_code)
    await verification_service.create(db=db, create_schema=verification_code_schema, user_id=user.id)
    await email_client.send_mail(recepients=[user.email], body=verify_code)
    return user


async def login(user: User, login_schema: UserLogin) -> dict:
    if not verify_password(
        plain_password=login_schema.password,
        hashed_password=user.password,
    ):
        raise Exception("User password is wrong!")
    subject = TokenSubject(
        username=str(user.username),
        password=user.password,
    )
    return await create_tokens(subject)

async def verify_account(user: User, verification_code: str) -> None:

