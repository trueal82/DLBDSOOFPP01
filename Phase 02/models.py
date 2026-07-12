### All the domain models go here, what a mess

from dataclasses import dataclass
from datetime import datetime

@dataclass
class Habit:
    """The primary domain model for the habit tracker application."""
    id: int
    name: str
    description: str
    frequency: datetime  # e.g., "daily", "weekly"
    start_date: datetime  # ISO format date string

@dataclass
class HabitExceution:
    """Represents the execution of a habit on a specific datetime."""
    id: int
    habit_id: int
    date: datetime  # ISO format date string
    comment: str