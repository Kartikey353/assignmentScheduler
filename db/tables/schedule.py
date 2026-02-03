from __future__ import annotations
from beanie import Document, Link
from typing import List, Optional
from enum import Enum
from datetime import datetime
from Scheduler.db.tables.history import ExecutionHistory
from db.tables.target import Target


class ScheduleStatus(str, Enum):
    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETED = "completed"   # auto-stopped for window


class ScheduleType(str, Enum):
    INTERVAL = "interval"     # run every interval_seconds
    WINDOW = "window"  



class Schedule(Document):
    name: str
    target: Link[Target]

     # 🔹 what type of schedule this is
    schedule_type: ScheduleType

    # 🔹 INTERVAL scheduling
    interval_seconds: Optional[int] = None
    corn_job_id: Optional[str] = None
    cron: Optional[str] = None  

    # 🔹 WINDOW scheduling
    window_start_at: Optional[datetime] = None
    duration_seconds: Optional[int] = None
    window_end_at: Optional[datetime] = None


    # 🔹 state
    status: ScheduleStatus = ScheduleStatus.ACTIVE

    # 🔹 execution tracking
    last_run_at: Optional[datetime] = None
    next_run_at: Optional[datetime] = None

    created_at: datetime
    updated_at: datetime
    interval_history : Optional[List[ExecutionHistory]] = [] 
    window_history : Optional[List[ExecutionHistory]] = []
          
    timezone: str = "UTC"

    class Settings:
        name = "schedules"