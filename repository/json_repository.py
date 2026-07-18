"""
This is a simple, json based repo.
It assumes a single user process
For using with API / Multiuser it is not recommended
due to missing synch / file locking

Although it is closely related to the inMemoryRepo, and
considering the DRY principle, not extracting certain methods
to a shared base class to avoid complexity and maintenance pain
"""
from datetime import timedelta, datetime

import config
from habit_json_serializer import HabitJsonSerializer
from models import Habit, ExecutionFrequency, HabitExecution
from repository.habit_repository import HabitRepository


class JsonRepository(HabitRepository):
    """Simple Json Repository"""

    def __init__(self):
        super().__init__()
        self.habits: list[Habit] = []
        self.serializer: HabitJsonSerializer = HabitJsonSerializer()
        self.habits = self.load_habits_from_disk()

    def update_habit(self, habit: Habit):
        updated_a_habit: bool = False
        for h in self.habits:
            if habit.id == h.id:
                updated_a_habit = True
                h.name = habit.name
                h.description = habit.description
        self.save()
        if not updated_a_habit:
            raise ValueError(f"No habit with given it {habit.id} found")

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
        all_habits.sort(key=lambda x: x.id)
        return all_habits[-1].id + 1

    def add_habit(self, habit) -> None:
        new_id = self.get_next_free_id()
        h = habit
        h.id = new_id
        self.habits.append(h)
        self.save()

    def delete_habit(self, habit_id) -> None:
        for habit in self.habits:
            if habit.id == habit_id:
                self.habits.remove(habit)
                break
        self.save()

    def get_habit_by_id(self, habit_id) -> Habit:
        for habit in self.habits:
            if habit.id == habit_id:
                return habit
        raise ValueError(f"No habit with given it {habit_id} found")

    def load_habits_from_disk(self):
        return self.serializer.read_from_file(config.JSON_FILE_PATH)

    def save(self):
        self.serializer.write_to_file(config.JSON_FILE_PATH, self.habits)

    def get_due_habits(self) -> list[Habit]:
        list_of_due_habits: list[Habit] = []
        for h in self.habits:
            e = h.executions
            e.sort(key=lambda x: x.date)
            if not h.executions:
                list_of_due_habits.append(h)
                continue
            last_execution: datetime = e[-1].date
            if h.frequency == ExecutionFrequency.DAILY:
                if not last_execution.day == datetime.today().day:
                    list_of_due_habits.append(h)
            elif h.frequency == ExecutionFrequency.WEEKLY:
                if datetime.today().day - last_execution.day >= timedelta(days=6):
                    list_of_due_habits.append(h)
        return list_of_due_habits

    def execute_habit(self, habit_id: int, comment: str) -> None:
        h: Habit = self.get_habit_by_id(habit_id)
        h_e_id = self.get_next_free_id_for_executions(h.executions)
        h.executions.append(HabitExecution(date=datetime.today(), comment=comment, habit_id=habit_id, id=h_e_id))
        self.update_habit(h)

    def get_next_free_id_for_executions(self, executions) -> int:
        if not executions:
            return 1
        executions.sort(key=lambda x: x.id)
        return executions[-1].id + 1
