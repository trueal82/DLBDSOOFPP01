from models import Habit
from repository.habit_repository import HabitRepository


class SQLiteRepository(HabitRepository):
    """
    SQLiteRepository is a dummy implementation of the HabitRepository interface.
    """

    def get_all_habits(self) -> list[Habit]:
        pass

    def get_habit_by_id(self, habit_id) -> Habit:
        pass

    def add_habit(self, habit: Habit):
        pass

    def update_habit(self, habit: Habit):
        pass

    def delete_habit(self, habit_id):
        pass

    def __init__(self, db_path):
        self.db_path = db_path
        pass  # Placeholder for future implementation
