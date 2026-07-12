from models import Habit
from repository.habit_repository import HabitRepository


class JsonRepository(HabitRepository):
    def __init__(self, file_path):
        self.file_path = file_path
        # Placeholder for future implementation
    
    def add_habit(self, habit: Habit):
        pass  # Placeholder for future implementation
    
    def delete_habit(self, habit_id):
        pass  # Placeholder for future implementation
    
    def get_all_habits(self) -> list[Habit]:
        pass  # Placeholder for future implementation

    def get_habit_by_id(self, habit_id) -> Habit:
        """Returns a habit by its ID."""
        pass
    
    def update_habit(self, habit: Habit):
        pass  # Placeholder for future implementation
