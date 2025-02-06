from dataclasses import dataclass
from typing import Optional, Dict, Any
from fastapi import HTTPException
from starlette import status


@dataclass
class ErrorInstance:
    detail: Optional[str]
    status_code: int


class APIError(HTTPException):
    def __init__(
        self, error: ErrorInstance, headers: Optional[Dict[str, Any]] = None
    ) -> None:
        super().__init__(status_code=error.status_code, detail=error.detail)
        self.error = error
        self.headers = headers


class BaseApplicationException(Exception):
    message: str = None

    def __init__(self, *args, **kwargs):
        assert self.message is not None
        super().__init__(self.message)


@dataclass
class InternalError(ErrorInstance):
    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail: str = "Something went wrong."


@dataclass
class InvalidChoice(ErrorInstance):
    status_code: int = status.HTTP_422_UNPROCESSABLE_ENTITY
    detail: str = "Invalid choice provided!"


class RandomNumberRetrievalError(BaseApplicationException):
    message: str = "Failure retrieving random number."
