
from repository.habit_repository import HabitRepository
from models import Habit, ExecutionFrequency
from datetime import datetime


class InMemoryRepository(HabitRepository):
    """Non-persistent repository, nice for testing"""

    def __init__(self):
        super().__init__()
        self.habits : list[Habit] = []
        self.habits.append(Habit(id=1, name="Brush teeth", description="Do it at least every day", frequency=ExecutionFrequency.DAILY, start_date=datetime.today()))
        self.habits.append(Habit(id=2, name="Wash feet", description="Do it at least every day", frequency=ExecutionFrequency.DAILY, start_date=datetime.today()))
    
    def update_habit(self, habit):
        pass

    def get_habits(self) -> list[Habit]:
        return self.habits
    
    def add_habit(self, habit) -> None:
        self.add_habit(habit)
    
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