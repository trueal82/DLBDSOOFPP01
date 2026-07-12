import config
from repository.habit_repository import HabitRepository

class SQLiteRepository(HabitRepository):
    """
    SQLiteRepository is a dummy implementation of the HabitRepository interface.
    """
    def __init__(self, db_path):
        pass  # Placeholder for future implementation