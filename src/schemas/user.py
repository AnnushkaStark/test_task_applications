from email_validator import validate_email
from pydantic import BaseModel, EmailStr, Field, validator

from constants.user import (
    MAX_PASSWORD_LENGTH,
    MAX_USERNAME_LENGTH,
    MIN_PASSWORD_LENGTH,
    MIN_USERNAME_LENGTH,
)


class UserBase(BaseModel):
    username: str = Field(
        min_length=MIN_USERNAME_LENGTH, max_length=MAX_USERNAME_LENGTH
    )
    email: EmailStr
    password: str = Field(
        max_length=MAX_PASSWORD_LENGTH, min_length=MIN_PASSWORD_LENGTH
    )


class UserCreate(UserBase):
    @validator("email")
    def email_check(cls, v: EmailStr) -> EmailStr:
        email_info = validate_email(v, check_deliverability=True)
        email = email_info.normalized
        return email


class UserLogin(BaseModel):
    email: str
    password: str
