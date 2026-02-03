import traceback
from datetime import datetime
from typing import List, Optional
from beanie import PydanticObjectId

from src.module.error.errors import Errors
from exception.base_error import BaseError 
from db.tables.target import Target
from db.tables.user import User
from src.module.dto.requests.create_target import TargetCreateRequest

class TargetService:
    """
    Service layer for managing HTTP Targets.
    Handles ownership by linking every target to a User.
    """

    @classmethod
    async def create_target(cls, target_data: TargetCreateRequest, email: str) -> Target:
        """
        Creates a new Target and links it to the requesting User.
        """
        try:
            # 1. Fetch the owner document
            user = await User.get(User.email == email)
            if not user:
                raise BaseError(
                    error=Errors.APPSER_DB_FIND_ERROR.value,
                    error_metadata=f"User with email {email} not found. Cannot assign target.",
                )

            # 2. Initialize the Target Document
            # model_dump() converts the Pydantic DTO into a dictionary for Beanie
            new_target = Target(
                **target_data.model_dump(),
                owner=user,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )

            # 3. Save to MongoDB
            await new_target.insert()

            # 4. Optional: Update the User's link list for faster bidirectional lookups
            if user.targets is None:
                user.targets = []
            user.targets.append(new_target)
            await user.save()

            return new_target

        except BaseError:
            raise
        except Exception:
            raise BaseError(
                error=Errors.APPSER_DB_INSERT_ERROR.value,
                error_metadata="Unexpected error during target creation",
                traceback=traceback.format_exc(),
            )

    @classmethod
    async def get_user_targets(cls, email: str) -> List[Target]:
        """
        Retrieves all targets belonging to a specific user.
        """
        try:
            # We filter by the owner's email
            user = await User.get(User.email == email)
            if not user:
                raise BaseError(
                    error=Errors.APPSER_DB_FIND_ERROR.value,
                    error_metadata=f"User with email {email} not found.",
                )
            return await Target.find(Target.owner.id == user.id).to_list()
            return await Target.find(Target.owner.id == user_id).to_list()
        except Exception:
            raise BaseError(
                error=Errors.APPSER_DB_FIND_ERROR.value,
                error_metadata=f"Failed to fetch targets for user {user_id}",
                traceback=traceback.format_exc(),
            )

    @classmethod
    async def get_target_by_id(cls, target_id: str, email: str) -> Optional[Target]:
        """
        Retrieves a single target by its ID, but ONLY if it belongs to the specified user.
        This provides a security layer against unauthorized access.
        """
        try:
            user = await User.get(User.email == email)
            if not user:
                raise BaseError(
                    error=Errors.APPSER_DB_FIND_ERROR.value,
                    error_metadata=f"User with email {email} not found.",
                )
            user_id = user.id
            target_oid = PydanticObjectId(target_id)
            return await Target.find_one(
                Target.id == target_oid,
                Target.owner.id == user_id
            )
        except Exception:
            raise BaseError(
                error=Errors.APPSER_DB_FIND_ERROR.value,
                error_metadata=f"Error fetching target {target_id}",
                traceback=traceback.format_exc(),
            )

    @classmethod
    async def delete_target(cls, target_id: str, email: str) -> bool:
        """
        Deletes a target after verifying ownership.
        """
        try:
            target = await cls.get_target_by_id(target_id, email)
            if not target:
                return False
            
            await target.delete()
            return True
        except Exception:
            raise BaseError(
                error=Errors.APPSER_DB_DELETE_ERROR.value,
                error_metadata=f"Failed to delete target {target_id}",
                traceback=traceback.format_exc(),
            )
        


    @classmethod
    async def update_target(cls, target_id: str, email: str, update_data: dict) -> Optional[Target]:
        """
        Updates target fields (URL, method, etc.) but prevents owner modification.
        """
        try:
            # 1. Resolve the user by email to ensure we have the correct owner context
            user = await User.find_one(User.email == email)
            if not user:
                raise BaseError(
                    error=Errors.APPSER_DB_FIND_ERROR.value,
                    error_metadata=f"User with email {email} not found.",
                )

            # 2. Find the target belonging to this specific user
            target_oid = PydanticObjectId(target_id)
            target = await Target.find_one(
                Target.id == target_oid,
                Target.owner.id == user.id
            )

            if not target:
                return None

            # 3. Filter out 'owner' or 'id' if they are accidentally passed in update_data
            # This ensures only the target configuration changes, not the ownership.
            allowed_updates = {
                k: v for k, v in update_data.items() 
                if k not in ["owner", "id", "_id", "created_at"]
            }

            # 4. Apply updates and refresh the 'updated_at' timestamp
            allowed_updates["updated_at"] = datetime.utcnow()
            
            # Using Beanie's .set() for an atomic update in MongoDB
            await target.set(allowed_updates)
            
            return target

        except Exception:
            raise BaseError(
                error=Errors.APPSER_DB_UPDATE_ERROR.value,
                error_metadata=f"Failed to update target {target_id} for user {email}",
                traceback=traceback.format_exc(),
            )