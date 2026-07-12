"""The domain models live here"""

from datetime import datetime
from enum import Enum

from pydantic import BaseModel


class Habit(BaseModel):
    """The primary domain model for the habit tracker application."""
    id: int | None  # Needs to be able to be none for new objects
    name: str
    description: str
    frequency: ExecutionFrequency  # e.g., "daily", "weekly"
    start_date: datetime  # ISO format date string


class HabitExecution(BaseModel):
    """Represents the execution of a habit on a specific datetime."""
    id: int
    habit_id: int
    date: datetime  # ISO format date string
    comment: str

class ExecutionFrequency(Enum):
    """Enum representing the execution frequency."""
    WEEKLY = "weekly"
    DAILY = "daily"
