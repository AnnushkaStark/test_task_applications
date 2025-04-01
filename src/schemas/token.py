from pydantic import BaseModel


class TokenAccessRefresh(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class TokenVerify(BaseModel):
    is_valid: bool


class TokenPayload(BaseModel):
    username: str
    password: str
