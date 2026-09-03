"""
Repository factory class to not make the service dependent on the repo impls.
"""
import config
from repository.habit_repository import HabitRepository
from repository.json_repository import JsonRepository


class RepositoryFactory:  # pylint: disable=too-few-public-methods
    """ A factory class to create repository instances based on the env configuration."""

    @staticmethod
    def get_repository(repo_type: str | None = None) -> HabitRepository:
        """
        Returns the repository instance for the given type. If no type is given
        it falls back to the HABIT_REPOSITORY environment variable / config.
        Args:
            repo_type: name of the repository implementation to instantiate
        Returns:
            an instance of the appropriate repository class
        Raises:
            ValueError: If no repository type is given/configured or the type
            is unknown.
        """
        if not repo_type:
            repo_type = config.HABIT_REPOSITORY

        if not repo_type:
            raise ValueError("HABIT_REPOSITORY is not set in the environment variables")
        if repo_type == "JsonRepository":
            return JsonRepository()

        raise ValueError(f"Unknown repository type: {repo_type}")
