from __future__ import annotations
from pydantic import BaseModel
from typing import Optional, Any
from requests import Response

"""
ref: https://www.wikiwand.com/en/List_of_HTTP_status_codes

Not considered:

406, 407, 411, 412, 414, 415, 417, 418, 421, 424, 425, 428,
505, 506, 510, 511

"""

errors = {
    400: "Bad Request",
    401: "Unauthorized",
    402: "Payment Required",
    403: "Forbidden",
    404: "Not Found",
    405: "Method Not Allowed",
    408: "Request Timeout",
    409: "Conflict",
    410: "Gone",
    413: "Payload Too Large",
    415: "Unsupported Media Type",
    422: "Unprocessable Content",
    423: "Locked",
    429: "Too Many Requests",
    430: "Security Rejection",
    431: "Request Header Fields Too Large",
    451: "Unavailable For Legal Reasons",
    498: "Invalid Token",
    499: "Token Required",
    500: "Internal Server Error",
    501: "Not Implemented",
    502: "Bad Gateway",
    503: "Service Unavailable",
    504: "Gateway Timeout",
    507: "Insufficient Storage",
    508: "Loop Detected",
}


class ErrorResponse(BaseModel):
    status: int
    detail: Optional[Any] = None

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        return f"{self.status}: {self.detail}"

    @staticmethod
    def parse(response: Response) -> ErrorResponse:
        status = response.status_code
        if status not in errors.keys():
            raise ValueError(
                f"Please submit a GitHub Issue, unknown response code: {response.status_code}"
            )
        else:
            if len(response.text):
                detail = response.json()["detail"]
            else:
                detail = errors[status]
            return ErrorResponse(status=status, detail=detail)
