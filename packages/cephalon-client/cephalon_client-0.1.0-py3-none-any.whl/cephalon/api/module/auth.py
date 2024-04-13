import requests
from requests import Response
from requests.exceptions import HTTPError
from typing import Any
from pydantic import ValidationError, BaseModel
from result import Result, Ok, Err
from cephalon.api.common.response_errors import ErrorResponse
from cephalon.api.schema.auth import (
    RegisterPayload,
    ResendPayload,
    ConfirmPayload,
    SetupPayload,
    SetupResult,
)


class Auth:
    def __init__(self, state: Any) -> None:
        self.state = state

    def register(
        self,
        email: str,
        password: str,
    ) -> Result[str, str]:
        """
        Start the registration process for a new account.

        Args:
            email (str): email address
            password (str): secure password
        """
        payload = RegisterPayload(email=email, password=password)
        response = requests.post(
            url=f"{self.state.get('endpoint')}/auth/register",
            json=payload.model_dump(),
        )
        if response.status_code == 200:
            return Ok(
                "If this user is not already registered, a confirmation email has been sent."
            )
        else:
            return Err(str(ErrorResponse.parse(response=response)))

    def resend(
        self,
        email: str,
    ) -> Result[str, str]:
        """
        Resend email with confirmation code.

        Args:
            email (str): email address
        """
        payload = ResendPayload(email=email)
        response = requests.post(
            url=f"{self.state.get('endpoint')}/auth/resend",
            json=payload.model_dump(),
        )
        if response.status_code == 200:
            return Ok(
                "If this user is registered, a confirmation email has been resent."
            )
        else:
            return Err(str(ErrorResponse.parse(response=response)))

    def confirm(
        self,
        email: str,
        code: str,
    ) -> Result[str, str]:
        """
        Confirm a newly registered account.

        Args:
            email (str): email address
            code (str): 6 digit confirmation code from email
        """
        payload = ConfirmPayload(email=email, code=code)
        response = requests.post(
            url=f"{self.state.get('endpoint')}/auth/confirm",
            json=payload.model_dump(),
        )
        if response.status_code == 200:
            if response.json():
                return Ok("User email confirmed.")
            else:
                return Err(
                    "Error encountered, please try again or submit a GitHub Issue."
                )
        else:
            return Err(str(ErrorResponse.parse(response=response)))

    # # this is login but with the expectation of MFA_SETUP
    # def setup(self, email: str, password: str) -> SetupResult:
    #     """"""
    #     ...

    # def validate(self, session: str, otp: str) -> ValidateResult:
    #     """
    #     Verify MFA code
    #     """
    #     ...

    # def login(self, email: str, password: str, otp: str) -> LoginResult:
    #     """"""
    #     ...

    # def logout(self) -> LogoutResult:
    #     """
    #     Remove local credentials/token and revoke tokens.
    #     """
    #     ...

    # def forgot(self) -> Result[str, str]:
    #     """Recover account"""
    #     ...

    # def revoke(self) -> Result[str, str]:
    #     raise NotImplementedError()

    # def refresh(self) -> Result[str, str]:
    #     """Run login and set new token in state."""
    #     ...

    # def _login_start(
    #     self,
    #     email: Optional[str] = None,
    #     password: Optional[str] = None,
    # ) -> Result[str, str]:
    #     email = self.state["email"] if email is None else email
    #     password = self.state["password"] if password is None else password
    #     if email is None:
    #         return Err("Missing email.")
    #     if password is None:
    #         return Err("Missing password.")
    #     payload = self.__login_start(LoginStartInput(email=email, password=password))
    #     if payload.result == "failure":
    #         return Err("Invalid credentials or server error.")
    #     elif payload.result == "success":
    #         self.state["token"] = payload.token
    #         return Ok("Successful login.")
    #     elif payload.result == "challenge":
    #         if payload.challenge == "NEW_PASSWORD_REQUIRED":
    #             raise
    #         elif payload.challenge == "MFA_SETUP":
    #             raise NotImplementedError()
    #         elif payload.challenge == "SOFTWARE_TOKEN_MFA":
    #             self.state["email"] = email
    #             self.state["session"] = payload.session
    #             return Ok(
    #                 "MFA Challenge: Please call the '.login_mfa' method with your OTP code."
    #             )
    #         else:
    #             raise
    #     else:
    #         raise

    # def _login_mfa(
    #     self,
    #     code: str,
    #     email: Optional[str] = None,
    #     session: Optional[str] = None,
    # ) -> Result[str, str]:
    #     email = self.state["email"] if email is None else email
    #     session = self.state["session"] if session is None else session
    #     if email is None:
    #         return Err("Missing email.")
    #     if session is None:
    #         return Err("Missing session.")
    #     payload = self.__login_mfa(
    #         LoginMfaInput(email=email, code=code, session=session)
    #     )
    #     if payload.result == "failure":
    #         return Err("Invalid credentials or server error.")
    #     elif payload.result == "success":
    #         self.state["email"] = email
    #         self.state["session"] = None
    #         self.state["token"] = payload.token
    #         return Ok("Successful login.")
    #     else:
    #         raise

    def _setup_password(self): ...

    def _setup_mfa(self): ...
