from typing import Literal, Optional
from pydantic import BaseModel, field_validator
from email_validator import validate_email, EmailNotValidError
from cephalon import utils

ServerError = Literal["InternalServerError", "RateLimit"]


class BaseEmailPayload(BaseModel):
    email: str

    @field_validator("email")
    def __validate_email(cls, email: str) -> str:
        try:
            email_info = validate_email(email)
            email = email_info.normalized
        except EmailNotValidError as invalid_email_error:
            raise ValueError(str(invalid_email_error))
        return email


class BaseEmailPasswordPayload(BaseEmailPayload):
    password: str

    @field_validator("password")
    def __validate_password(cls, password: str) -> str:
        password_check = utils.validate_password(password)
        if not password_check.valid:
            raise ValueError(str(password_check.errors))
        return password


class BaseResult(BaseModel):
    ok: bool
    msg: Optional[str] = None
    err: Optional[ServerError] = None
