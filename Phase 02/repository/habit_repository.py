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
        pass

    @abstractmethod
    def get_habit_by_id(self, habit_id) -> Habit:
        """Returns a habit by its ID."""
        pass

    @abstractmethod
    def add_habit(self, habit: Habit):
        """Adds a new habit to the repository."""
        pass

    @abstractmethod
    def update_habit(self, habit: Habit):
        ### TODO: Decide if we want this.
        pass

    @abstractmethod
    def delete_habit(self, habit_id):
        ### TODO: Decide if we want this.
        pass