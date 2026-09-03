"""
The main service for clients(TUIs, APIs, ...) to interact with
"""

from datetime import date, datetime

from models.models import ExecutionFrequency, Habit
from repository.habit_repository import HabitRepository
from repository.repo_factory import RepositoryFactory
from utils import analytics
from utils.analytics import Streak


class HabitService:
    """This is the main service for clients(TUIs, APIs,...) to interact with"""

    def __init__(self, repository_type: str | None = None,
                 repository: HabitRepository | None = None):
        """Creates a service on top of the given repository. If none is given,
        one is created via the RepositoryFactory (from repository_type or the
        configured default)."""
        if repository is not None:
            self.repository: HabitRepository = repository
        else:
            self.repository = RepositoryFactory.get_repository(repository_type)

    def get_all_habits(self) -> list[Habit]:
        """
        Returns:
            list[Habit]: all habits
        """
        return self.repository.get_all_habits()

    def get_habit_by_id(self, habit_id: int) -> Habit:
        """
        Returns:
            Habit: the habit with the given id
        :raises ValueError: if no habit with the given id exists
        """
        return self.repository.get_habit_by_id(habit_id)

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
                  start_date: datetime | None = None) -> Habit:
        """
        Creates a new habit and persists it.

        :param name: the habit's name, must not be empty
        :param frequency: "daily" or "weekly"
        :param description: optional description
        :param start_date: optional start date, defaults to now
        :return: the persisted habit, including its assigned id
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
        habit: Habit = Habit(name=name, description=description, frequency=frequency,
                             start_date=start_date, id=None)
        self.repository.add_habit(habit)
        return habit

    def update_habit(self, habit: Habit) -> None:
        """Persists changes made to the given habit.
        :raises ValueError: if no habit with the given id exists"""
        self.repository.update_habit(habit)

    def delete_habit(self, habit_id: int) -> None:
        """Deletes the habit with the given id.
        :raises ValueError: if no habit with the given id exists"""
        self.repository.delete_habit(habit_id)

    def get_due_habits(self, today: date | None = None) -> list[Habit]:
        """Returns a list of all habits that are due on the given day
        (defaults to today)."""
        return self.repository.get_due_habits(today)

    def execute_habits(self, habit_id: int, comment: str) -> None:
        """Marks the habit with the given id as done today."""
        self.repository.execute_habit(habit_id=habit_id, comment=comment)

    def get_habits_by_periodicity(self, frequency: str) -> list[Habit]:
        """Returns all habits with the given periodicity ("daily"/"weekly").
        :raises ValueError: if the frequency is invalid"""
        return analytics.get_habits_by_periodicity(
            self.repository.get_all_habits(), self._to_frequency(frequency))

    def get_longest_streak_all(self) -> Streak | None:
        """Returns the longest run streak of all defined habits,
        or None if no habit was ever executed."""
        return analytics.get_longest_streak_all(self.repository.get_all_habits())

    def get_longest_streak_for_habit(self, habit_id: int) -> Streak | None:
        """Returns the longest run streak of the habit with the given id,
        or None if it was never executed.
        :raises ValueError: if no habit with the given id exists"""
        return analytics.get_longest_streak_for_habit(
            self.repository.get_habit_by_id(habit_id))

    @staticmethod
    def _to_frequency(frequency: str) -> ExecutionFrequency:
        """Converts a frequency string into an ExecutionFrequency.
        :raises ValueError: if the frequency is invalid"""
        try:
            return ExecutionFrequency(frequency)
        except ValueError as e:
            raise ValueError("invalid habit frequency") from e
