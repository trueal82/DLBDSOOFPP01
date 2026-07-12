from repository.repo_factory import RepositoryFactory
from repository.habit_repository import HabitRepository

from models import Habit

class HabitService:
    """This is the main service for clients(TUIs, APIs,...) to interact with"""
    def __init__(self):
        self.repository: HabitRepository = RepositoryFactory.get_repository()

    def get_all_habits(self) -> list[Habit]:
        """
        Returns:
            list[Habit]: all habits
        """
        return self.repository.get_all_habits()
    