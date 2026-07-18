"""
Abstract base class for habit repositories.
"""
from abc import ABC, abstractmethod

from models import Habit


class HabitRepository(ABC):
    """
    Abstract base class for habit repositories.
    Defines the interface for habit repository implementations.
    """

    @abstractmethod
    def get_all_habits(self) -> list[Habit]:
        """Returns a list of all habits."""

    @abstractmethod
    def get_habit_by_id(self, habit_id) -> Habit:
        """Returns a habit by its ID."""

    @abstractmethod
    def add_habit(self, habit: Habit):
        """Adds a new habit to the repository."""

    @abstractmethod
    def update_habit(self, habit: Habit):
        """Updates the habit in the repository."""
        ### TODO: Decide if we want this.

    @abstractmethod
    def delete_habit(self, habit_id):
        """Deletes the habit from the repository."""
        ### TODO: Decide if we want this.

    @abstractmethod
    def get_due_habits(self) -> list[Habit]:
        """Returns a list of all due habits."""

    @abstractmethod
    def execute_habit(self, habit_id: int, comment: str) -> None:
        """Execute a habit and update the habit in the repository."""
