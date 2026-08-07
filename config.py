"""
Basic configuration for the tool
"""
import os

from dotenv import load_dotenv

load_dotenv()

# Logging configuration
LOG_LEVEL = os.getenv("LOGGING_LEVEL", "INFO")

# Repository configuration
HABIT_REPOSITORY = os.getenv("HABIT_REPOSITORY", "JsonRepository")
JSON_FILE_PATH = os.getenv("JSON_FILE_PATH", "./data/repository.json")
