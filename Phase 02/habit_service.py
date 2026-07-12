from repository.repo_factory import RepositoryFactory
from repository.habit_repository import HabitRepository

class HabitService:
    def __init__(self):
        self.repository: HabitRepository = RepositoryFactory.get_repository()
        pass  # Placeholder for future implementation