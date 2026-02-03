from pydantic import BaseModel, HttpUrl, Field
from typing import Dict, Optional
from db.tables.target import HttpMethod

class TargetCreateRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    url: str # Using str for flexible template URLs, or use HttpUrl for strict validation
    method: HttpMethod = HttpMethod.GET
    headers: Dict[str, str] = {}
    body_template: Optional[Dict] = None

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Production Health Check",
                "url": "https://api.myapp.com/v1/health",
                "method": "GET",
                "headers": {"Authorization": "Bearer token"},
                "body_template": {"status": "checking"}
            }
        }