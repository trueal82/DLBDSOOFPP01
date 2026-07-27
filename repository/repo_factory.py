"""
Repository factory class to not make the service dependent on the repo impls.
"""
import config
from repository.habit_repository import HabitRepository
from repository.json_repository import JsonRepository


class RepositoryFactory:
    """ A factory class to create repository instances based on the env configuration."""

    @staticmethod
    def get_repository() -> HabitRepository:
        """
        Returns the configured repository instance based on the HABIT_REPOSITORY
        environment variable
        Returns:
            an instance of the appropriate repository class
        Raises:
            ValueError: If the HABIT_REPOSITORY environment variable is not set or
            has an unknown value.
        """
        repo_type = config.HABIT_REPOSITORY

        if not repo_type:
            raise ValueError("HABIT_REPOSITORY is not set in the environment variables")
        elif repo_type == "JsonRepository":
            return JsonRepository()

        raise ValueError(f"Unknown repository type: {repo_type}")
