from pydantic import BaseModel


class VerificationCodeBase(BaseModel):
    verification_code: str


class VerificationCodeCreate(VerificationCodeBase):
    ...


class VerificationCodeCreateDB(VerificationCodeCreate):
    user_id: int
