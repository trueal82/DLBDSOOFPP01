### All the domain models go here, what a mess

from pydantic import BaseModel
from datetime import datetime
from enum import Enum

class Habit(BaseModel):
    """The primary domain model for the habit tracker application."""
    id: int
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
    WEEKLY = "weekly"
    DAILY = "daily"