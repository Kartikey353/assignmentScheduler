from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class UserCreateRequest(BaseModel):
    # Required and validated as a real email format
    email: EmailStr
    
    # Required password (we use 'password' here, but hash it before DB)
    password: str = Field(..., min_length=8)
    
    # Optional field 
    full_name: Optional[str] = None

    class Config:
        # This provides a helpful example in your FastAPI Swagger docs
        json_schema_extra = {
            "example": {
                "email": "kartik@example.com",
                "password": "securepassword123",
                "full_name": "Kartikey Bhardwaj"
            }
        }