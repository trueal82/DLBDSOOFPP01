"""
Abstract base class for habit repositories.
"""
from abc import ABC, abstractmethod
from datetime import date

from models.models import Habit


class HabitRepository(ABC):
    """
    Abstract base class for habit repositories.
    Defines the interface for habit repository implementations.
    """

    @abstractmethod
    def get_all_habits(self) -> list[Habit]:
        """Returns a list of all habits."""

    @abstractmethod
    def get_habit_by_id(self, habit_id: int) -> Habit:
        """Returns a habit by its ID.
        :raises ValueError: if no habit with the given id exists"""

    @abstractmethod
    def add_habit(self, habit: Habit) -> Habit:
        """Adds a new habit to the repository, assigns its id and returns it."""

    @abstractmethod
    def update_habit(self, habit: Habit) -> None:
        """Persists changes made to the given habit.
        :raises ValueError: if no habit with the given id exists"""

    @abstractmethod
    def delete_habit(self, habit_id: int) -> None:
        """Deletes the habit with the given id from the repository.
        :raises ValueError: if no habit with the given id exists"""

    @abstractmethod
    def get_due_habits(self, today: date | None = None) -> list[Habit]:
        """Returns a list of all habits that are due on the given day
        (defaults to today)."""

    @abstractmethod
    def execute_habit(self, habit_id: int, comment: str) -> None:
        """Execute a habit and update the habit in the repository."""
