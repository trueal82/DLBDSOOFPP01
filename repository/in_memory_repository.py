"""
This is a simple, non-persistent repo
"""
from datetime import datetime

from models import Habit, ExecutionFrequency
from repository.habit_repository import HabitRepository


class InMemoryRepository(HabitRepository):
    """Non-persistent repository, nice for testing"""

    def __init__(self):
        super().__init__()
        self.habits: list[Habit] = []
        self.habits.append(Habit(id=1, name="Brush teeth", description="Do it at least every day",
                                 frequency=ExecutionFrequency.DAILY, start_date=datetime.today()))
        self.habits.append(Habit(id=2, name="Wash feet", description="Do it at least every day",
                                 frequency=ExecutionFrequency.DAILY, start_date=datetime.today()))

    def update_habit(self, habit: Habit):
        updated_a_habit: bool = False
        for h in self.habits:
            if habit.id == h.id:
                updated_a_habit = True
                h.name = habit.name
                h.description = habit.description
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
        all_habits.sort(key=lambda x: x.id)
        return all_habits[-1].id + 1

    def add_habit(self, habit) -> None:
        new_id = self.get_next_free_id()
        h = habit
        h.id = new_id
        self.habits.append(h)

    def delete_habit(self, habit_id) -> None:
        for habit in self.habits:
            if habit.id == habit_id:
                self.habits.remove(habit)
                break

    def get_habit_by_id(self, habit_id) -> Habit:
        for habit in self.habits:
            if habit.id == habit_id:
                return habit
        raise ValueError(f"No habit with given it {habit_id} found")
