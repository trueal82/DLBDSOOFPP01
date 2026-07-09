from repo_factory import RepositoryFactory

class HabitService:
    def __init__(self):
        self.repository = RepositoryFactory.get_repository()
        pass  # Placeholder for future implementation