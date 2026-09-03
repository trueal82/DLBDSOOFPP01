"""
This is a simple, json based repo.
It assumes a single user process
For using with API / Multiuser it is not recommended
due to missing synch / file locking

"""
from datetime import date, datetime

import config
from models.models import Habit, ExecutionFrequency, HabitExecution
from repository.habit_repository import HabitRepository
from utils.habit_json_serializer import HabitJsonSerializer


class JsonRepository(HabitRepository):
    """Simple Json Repository"""

    def __init__(self, json_file_path: str | None = None):
        """
        :param json_file_path: Can be proviced directly, but if omitted it
        will be read from the config
        """
        if not json_file_path:
            self.json_file_path = config.JSON_FILE_PATH
        else:
            self.json_file_path = json_file_path
        self.habits: list[Habit] = []
        self.serializer: HabitJsonSerializer = HabitJsonSerializer()
        self.habits = self.load_habits_from_disk()

    def update_habit(self, habit: Habit) -> None:
        """Persists the given habit's state. The repository stores the same
        objects its getters return, so in-place changes only need saving."""
        stored: Habit | None = next((h for h in self.habits if h.id == habit.id), None)
        if stored is None:
            raise ValueError(f"No habit with given id {habit.id} found")
        self.save()

    def get_all_habits(self) -> list[Habit]:
        return self.habits

    def get_next_free_id(self) -> int:
        """
        Determine the next free habit id from the internal representation.
        :return:
        """
        all_habits = self.get_all_habits()
        if not all_habits:
            return 1
        return max(habit.id for habit in all_habits) + 1

    def add_habit(self, habit: Habit) -> Habit:
        habit.id = self.get_next_free_id()
        self.habits.append(habit)
        self.save()
        return habit

    def delete_habit(self, habit_id: int) -> None:
        habit: Habit = self.get_habit_by_id(habit_id)
        self.habits.remove(habit)
        self.save()

    def get_habit_by_id(self, habit_id: int) -> Habit:
        habit: Habit | None = next((h for h in self.habits if h.id == habit_id), None)
        if habit is None:
            raise ValueError(f"No habit with given id {habit_id} found")
        return habit

    def load_habits_from_disk(self) -> list[Habit]:
        """Loads the habits from the configured json file."""
        return self.serializer.read_from_file(self.json_file_path)

    def save(self) -> None:
        """Persists all habits to the configured json file."""
        self.serializer.write_to_file(self.json_file_path, self.habits)

    def get_due_habits(self, today: date | None = None) -> list[Habit]:
        """Returns all habits due on the given day. A habit is due if it was
        never executed, or its last execution lies in an earlier period
        (earlier day for daily habits, earlier ISO week for weekly ones)."""
        if today is None:
            today = datetime.today().date()
        due_habits: list[Habit] = []
        for habit in self.habits:
            if not habit.executions:
                due_habits.append(habit)
                continue
            last_execution_date: date = max(
                execution.date for execution in habit.executions).date()
            if habit.frequency == ExecutionFrequency.DAILY:
                if last_execution_date < today:
                    due_habits.append(habit)
            elif habit.frequency == ExecutionFrequency.WEEKLY:
                if last_execution_date.isocalendar()[:2] < today.isocalendar()[:2]:
                    due_habits.append(habit)
        return due_habits

    def execute_habit(self, habit_id: int, comment: str) -> None:
        """Appends a new execution (now, with the given comment) to the habit
        with the given id and persists it.
        :raises ValueError: if no habit with the given id exists"""
        habit: Habit = self.get_habit_by_id(habit_id)
        execution_id = self.get_next_free_id_for_executions(habit.executions)
        habit.executions.append(
            HabitExecution(date=datetime.today(), comment=comment,
                           habit_id=habit_id, id=execution_id))
        self.save()

    @staticmethod
    def get_next_free_id_for_executions(executions: list[HabitExecution]) -> int:
        """Determine the next free execution id for the given executions."""
        if not executions:
            return 1
        return max(execution.id for execution in executions) + 1
