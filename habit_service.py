"""
The main service for clients(TUIs, APIs, ...) to interact with
"""

from datetime import datetime

from models import ExecutionFrequency
from models import Habit
from repository.habit_repository import HabitRepository
from repository.repo_factory import RepositoryFactory


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

    def get_execution_frequencies(self) -> list[str]:
        """
        Primarily intended for clients to populate the list if frequencies
        Returns:
            list[str]: all execution frequencies
        """
        return [frequency.value for frequency in ExecutionFrequency]

    def add_habit(self,
                  name: str,
                  frequency: str,
                  description: str | None = None,
                  start_date: datetime | None = None):
        """
        Args:
        :param name:
        :param frequency:
        :param description:
        :param start_date:
        :return:
        :raises ValueError: if frequency is invalid
        :raises ValueError: if name is empty
        """
        if not name:
            raise ValueError("new habits must specify name")
        if not description:
            description = ""
        if not frequency:
            raise ValueError("new habits must specify frequency")
        try:
            frequency = ExecutionFrequency(frequency)
        except ValueError as e:
            raise ValueError("invalid habit frequency") from e
        if not start_date:
            start_date = datetime.today()
        habit:Habit = Habit(name=name, description=description, frequency=frequency,
                            start_date=start_date, id=None)
        self.repository.add_habit(habit)
