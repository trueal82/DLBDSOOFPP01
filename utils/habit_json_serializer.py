"""
Import and Export class for Habit
"""
import logging
import pathlib
from pathlib import Path

from pydantic import TypeAdapter
from pydantic_core import PydanticSerializationError

from models.models import Habit


class HabitJsonSerializer:
    """
    Serializer for Habit object
    """

    def __init__(self):
        self.logging: logging.Logger = logging.getLogger(__name__)

    def read_from_file(self, filename: str) -> list[Habit]:
        """
        Read the habit list from a file
        :param filename: the filename:
        :return: a list of habit objects
        :raises Exception: if an error occurred while reading the habit list
        """
        path = Path(filename)

        if not path.exists():
            return []

        json_string = path.read_text(encoding="utf-8")
        habit_list_adapter = TypeAdapter(list[Habit])
        habits = habit_list_adapter.validate_json(json_string)
        return habits

    def write_to_file(self, filename: str, habits: list[Habit]) -> None:
        """
        Write the habit list to a file
        :param habits: list of habit objects
        :param filename: the filename
        :return:
        :raises Exception: if an error occurred while saving the habit list
        """
        habit_list_adapter = TypeAdapter(list[Habit])
        try:
            json_data = habit_list_adapter.dump_json(
                habits,
                indent=2,
            )
        except PydanticSerializationError as e:
            self.logging.error("An error occurred while saving habit list: %s", e)
            raise
        p = pathlib.Path(filename)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(json_data)
