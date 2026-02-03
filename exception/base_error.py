from typing import Dict, Optional
from utils.logger import get_logger
from pydantic import BaseModel

logger = get_logger("BaseError")


class BaseError(Exception):
    def __init__(
        self,
        error: Dict[str, str],
        traceback: Optional[str] = None,
        error_metadata: Optional[str] = None,
    ) -> None:
        self.error_type = error["type"]
        self.error_message = error["message"]
        self.error_metadata = error_metadata
        self.traceback = traceback

        # Log inside __init__ using self.*
        logger.error(
            "[BaseError] type=%s | message=%s | metadata=%s\nTraceback:\n%s",
            self.error_type,
            self.error_message,
            self.error_metadata or "N/A",
            self.traceback or "N/A",
        )

        super().__init__(
            self.error_type, self.error_message, self.error_metadata, self.traceback
        )

    def __str__(self) -> str:
        return "{}: {}\n{}\n{}".format(
            self.error_type,
            self.error_message,
            self.error_metadata or "No metadata",
            self.traceback or "No traceback",
        )


class _ErrorDetail(BaseModel):
    type: str
    message: str


class BaseErrorResponse(BaseModel):
    detail: _ErrorDetail
