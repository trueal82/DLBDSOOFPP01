"""The domain models live here"""
from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, Field, field_validator


class ExecutionFrequency(StrEnum):
    """Enum representing the execution frequency of a habit."""
    DAILY = "daily"
    WEEKLY = "weekly"


class HabitExecution(BaseModel):
    """Represents the execution of a habit on a specific datetime."""
    id: int | None  # Needs to be able to be none for new objects with certain repositories
    habit_id: int
    date: datetime  # ISO format date string
    comment: str


class Habit(BaseModel):
    """The primary domain model for the habit tracker application."""
    id: int | None = None  # Needs to be able to be none for new objects with certain repositories
    name: str
    description: str
    frequency: ExecutionFrequency  # "daily" or "weekly"
    start_date: datetime  # ISO format date string
    executions: list[HabitExecution] = Field(default_factory=list)

    @field_validator("name")
    @classmethod
    def name_must_not_be_empty(cls, value: str) -> str:
        """Rejects empty or whitespace-only habit names."""
        if not value.strip():
            raise ValueError("habit name must not be empty")
        return value
