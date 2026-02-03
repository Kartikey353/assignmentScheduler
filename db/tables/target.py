from __future__ import annotations
from beanie import Document, Link
from typing import Dict, Optional
from enum import Enum 
from datetime import datetime

class HttpMethod(str, Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    DELETE = "DELETE" 


class Target(Document):
    name: str
    url: str
    method: HttpMethod
    headers: Dict[str, str] = {}
    body_template: Optional[Dict] = None  # JSON template
    created_at: datetime
    updated_at: datetime

    class Settings:
        name = "targets"