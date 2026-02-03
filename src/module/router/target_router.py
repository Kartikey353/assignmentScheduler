from fastapi import APIRouter, Depends, status, Header, Path, Body
from fastapi.responses import JSONResponse
from typing import List, Optional, Dict

from src.module.service.target_service import TargetService
from src.module.dto.requests.create_target import TargetCreateRequest
from src.module.error.client_error import ClientError as ClientErrorEnum
from utils.logger import get_logger
from db.tables.target import Target

logger = get_logger("TargetRouter")

router = APIRouter(prefix="/target")

@router.post("/createTarget", status_code=status.HTTP_201_CREATED)
async def create_target(
    request: TargetCreateRequest,
    email: str = Header(..., description="User email for identification"),
    service: TargetService = Depends(TargetService)
):
    """
    Create a new HTTP target for the user.
    """
    try:
        # Assuming TargetService is a class with class methods based on inspection, 
        # or instance methods. Looking at target_service.py, they are @classmethods.
        # But we can also instantiate it if needed, or call directly.
        # The Depends(TargetService) injection suggests we might want to use it as an instance
        # if dependencies are needed later. However, the service methods are class methods.
        # I will call them on the class for now as per the file content I saw.
        
        result = await TargetService.create_target(request, email)
        return result
    except Exception as e:
        logger.error(f"Error creating target: {e}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=ClientErrorEnum.APP_INTERNAL_SERVER_ERROR.value,
        )

@router.get("/userTargets", response_model=List[Target])
async def get_user_targets(
    email: str = Header(..., description="User email for identification")
):
    """
    Get all targets for the verified user.
    """
    try:
        results = await TargetService.get_user_targets(email)
        return results
    except Exception as e:
        logger.error(f"Error fetching user targets: {e}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=ClientErrorEnum.APP_INTERNAL_SERVER_ERROR.value,
        )

@router.get("/{target_id}", response_model=Optional[Target])
async def get_target(
    target_id: str = Path(..., description="The ID of the target"),
    email: str = Header(..., description="User email for identification")
):
    """
    Get a specific target by ID.
    """
    try:
        target = await TargetService.get_target_by_id(target_id, email)
        if not target:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={"message": "Target not found"}
            )
        return target
    except Exception as e:
        logger.error(f"Error fetching target {target_id}: {e}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=ClientErrorEnum.APP_INTERNAL_SERVER_ERROR.value,
        )

@router.put("/{target_id}", response_model=Optional[Target])
async def update_target(
    target_id: str = Path(..., description="The ID of the target"),
    update_data: Dict = Body(..., description="Fields to update"),
    email: str = Header(..., description="User email for identification")
):
    """
    Update a target.
    """
    try:
        updated_target = await TargetService.update_target(target_id, email, update_data)
        if not updated_target:
             return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={"message": "Target not found or not authorized"}
            )
        return updated_target
    except Exception as e:
        logger.error(f"Error updating target {target_id}: {e}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=ClientErrorEnum.APP_INTERNAL_SERVER_ERROR.value,
        )

@router.delete("/{target_id}")
async def delete_target(
    target_id: str = Path(..., description="The ID of the target"),
    email: str = Header(..., description="User email for identification")
):
    """
    Delete a target.
    """
    try:
        success = await TargetService.delete_target(target_id, email)
        if not success:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={"message": "Target not found or not authorized"}
            )
        return {"message": "Target deleted successfully", "id": target_id}
    except Exception as e:
        logger.error(f"Error deleting target {target_id}: {e}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=ClientErrorEnum.APP_INTERNAL_SERVER_ERROR.value,
        )
