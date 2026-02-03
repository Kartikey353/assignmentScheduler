from src.module.dto.requests.create_user import UserCreateRequest
from fastapi import APIRouter, Depends, status, Path
from src.module.service.user_service import UserService
from src.module.error.client_error import ClientError as ClientErrorEnum
from fastapi.responses import JSONResponse
from utils.logger import get_logger

logger = get_logger("UserRouter")

router = APIRouter(prefix="/user")


@router.post("/createUser", status_code=status.HTTP_201_CREATED)
async def create_user(
    request: UserCreateRequest,
    service: UserService = Depends(UserService)
):
    try:
        result = await service.create_user(request)
        return result
    except Exception as e:
        logger.error(f"Error creating user: {e}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=ClientErrorEnum.APP_INTERNAL_SERVER_ERROR.value,
        )
