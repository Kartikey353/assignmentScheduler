from enum import Enum


class ClientError(Enum):
    APP_VALIDATION_ERROR = {
        "status_code": "400",
        "content": {"message": "Validation Error (check the request payload)"},
    }
    APP_INTERNAL_SERVER_ERROR = {
        "status_code": "500",
        "content": {"message": "Internal Server Error"},
    }
    APP_NOT_FOUND_ERROR = {
        "status_code": "404",
        "content": {"message": "Data Not Found"},
    }
    APP_UNAUTHORIZED_ERROR = {
        "status_code": "403",
        "content": {
            "message": "unauthorized action made you are not allowed to perform this action"
        },
    }
