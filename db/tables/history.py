from __future__ import annotations
from beanie import Document, Link, PydanticObjectId
from typing import Optional, Dict, Any
from enum import Enum
from datetime import datetime
from db.tables.schedule import Schedule, ScheduleType

class ExecutionStatus(str, Enum):
    COMPLETED = "completed"
    INTERRUPTED = "interrupted"
    FAILED = "failed"

class ExecutionHistory(Document):
    schedule_id: PydanticObjectId  # Reference to the parent schedule
    schedule_name: str             # Snapshot of name (useful if schedule is deleted)
    task_type: ScheduleType        # INTERVAL or WINDOW
    
    # Timing
    start_time: datetime
    end_time: datetime
    latency_ms: float              # Total execution time in milliseconds
    
    # Response Data
    status: ExecutionStatus
    status_code: Optional[int] = None
    response_body: Optional[str] = None
    error_log: Optional[str] = None # Captures stack traces or exception messages
    
    # Metadata
    worker_id: str                 # Which of your 4 workers ran this?
    request_id: str                # Unique run ID for tracing
    

    class Settings:
        name = "execution_history"
        # We add indexes for fast searching by schedule or time
        indexes = [
            "schedule_id",
            "task_type",
            "start_time"
        ]