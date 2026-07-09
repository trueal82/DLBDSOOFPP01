from json_repository import JsonRepository
from sqlite_repository import SQLiteRepository
import config

class RepositoryFactory:
    """ A factory class to create repository instances based on the env configuration."""
    
    @staticmethod
    def get_repository():
        """
        Returns the configured repository instance based on the HABIT_REPOSITORY environment variable
        Returns:
            an instance of the appropriate repository class
        Raises:
            ValueError: If the HABIT_REPOSITORY environment variable is not set or has an unknown value.
        """
        repo_type = config.HABIT_REPOSITORY

        ### TODO for a few repos this way of organizing the code is fine, but for more repos we might want to use a dictionary mapping repo_type to class, so we don't have to keep adding elifs. But for now this is fine.

        if not repo_type:
            raise ValueError("HABIT_REPOSITORY is not set in the environment variables")
        
        if repo_type == "JsonRepository":
            return JsonRepository(config.JSON_FILE_PATH)
        
        elif repo_type == "SQLiteRepository":
            db_path = config.SQLITE_DB_PATH
            if not db_path:
                ### TODO can we even reach here? We set a default value for SQLITE_DB_PATH in config.py, so it should never be None. But let's keep this check for safety.
                raise ValueError("db_path must be provided for SQLiteRepository")
            return SQLiteRepository(db_path)
        
        else:
            raise ValueError(f"Unknown repository type: {repo_type}")