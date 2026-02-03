import traceback
from datetime import datetime
from pymongo.errors import DuplicateKeyError

# Assuming these are your internal imports
from src.module.error.errors import Errors
from exception.base_error import BaseError 
from src.module.dto.requests.create_user import UserCreateRequest 
from db.tables.user import User 
from utils.security import hash_password

# You'll need a hashing utility (e.g., passlib)
# from core.security import hash_password 

class UserService:
    
    async def get_user_by_email(self, email: str):
        """Find a user by their unique email."""
        try:
            # Beanie uses find_one for single document lookups
            user = await User.find_one(User.email == email)
            return user
        except Exception:
            raise BaseError(
                error=Errors.APPSER_DB_FIND_ERROR.value,
                error_metadata=f"Failed to find user with email: {email}",
                traceback=traceback.format_exc(),
            )
    
    async def create_user(self, user_data: UserCreateRequest):
        """Hashes password and inserts a new user into MongoDB."""
        try:
            hashed_pw = hash_password(user_data.password)
            
            user = User(
                email=user_data.email,
                full_name=user_data.full_name,
                hashed_password=hashed_pw
            ) 
            
            # 3. Insert into DB
            await user.insert()
            return user

        except DuplicateKeyError:
            raise BaseError(
                error=Errors.APPSER_DB_ALREADY_EXISTS.value, # Add this to your Errors enum
                error_metadata="A user with this email already exists",
                traceback=traceback.format_exc(),
            )
        except Exception:
            raise BaseError(
                error=Errors.APPSER_DB_INSERT_ERROR.value,
                error_metadata="Unexpected error during user creation",
                traceback=traceback.format_exc(),
            )