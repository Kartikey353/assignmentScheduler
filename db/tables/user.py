from __future__ import annotations
from beanie import Document, Link, Indexed
from typing import List, Optional, TYPE_CHECKING
from datetime import datetime
from pydantic import EmailStr, Field

# Use TYPE_CHECKING to avoid circular imports at runtime
if TYPE_CHECKING:
    from db.tables.target import Target
    from db.tables.schedule import Schedule

class User(Document):
    email: Indexed(EmailStr, unique=True)
    full_name: Optional[str] = None
    hashed_password: str
    
    # Use string names "Target" and "Schedule" instead of the classes
    targets: List[Link["Target"]] = []
    schedules: List[Link["Schedule"]] = []
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "users"