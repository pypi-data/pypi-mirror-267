from pydantic import BaseModel, field_validator
from typing import Optional
from cephalon import utils
from cephalon.api.common.base_schemas import (
    BaseEmailPayload,
    BaseEmailPasswordPayload,
    BaseResult,
)


class RegisterPayload(BaseEmailPasswordPayload): ...


class ResendPayload(BaseEmailPayload): ...


class ConfirmPayload(BaseEmailPayload):
    code: str

    @field_validator("code")
    def __validate_code(cls, code: str) -> str:
        # todo
        return code


class SetupPayload(BaseEmailPasswordPayload): ...


class SetupResult(BaseModel):
    secret: Optional[str] = None
    session: Optional[str] = None


class ValidatePayload(BaseModel):
    session: str
    otp: str


class ValidateResult(BaseResult): ...


class LoginPayload(BaseEmailPasswordPayload):
    otp: str


class LoginResult(BaseResult):
    token: Optional[str] = None
