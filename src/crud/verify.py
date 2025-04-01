from models import VerificationCode
from schemas.verify import VerificationCodeBase, VerificationCodeCreate

from .async_crud import BaseAsyncCRUD


class VerificationCodeCRUD(
    BaseAsyncCRUD[
        VerificationCode, VerificationCodeCreate, VerificationCodeBase
    ]
):
    ...


verification_code_crud = VerificationCodeCRUD(VerificationCode)
