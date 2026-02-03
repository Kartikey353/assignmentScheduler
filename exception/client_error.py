from typing import Optional

from fastapi import HTTPException
from pydantic import BaseModel
from utils.logger import get_logger

logger = get_logger("ClientError")


class ClientError(HTTPException):
    def __init__(
        self, status_code: int, message: str, log_exception: bool = False
    ) -> None:
        self.status_code = status_code
        self.message = message
        self.log_exception = log_exception
        super().__init__(status_code, message)

        logger.info(
            "[ClientError] status_code=%s | message=%s", self.status_code, self.message
        )


class _ErrorDetail(BaseModel):
    message: str


class ClientErrorResponse(BaseModel):
    detail: _ErrorDetail
