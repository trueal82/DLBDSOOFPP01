"""
Import and Export class for Habit
"""
import logging
import pathlib

from pydantic import TypeAdapter
from pydantic_core import PydanticSerializationError

from habit_service import HabitService
from models import Habit


class ImpEx():
    """
    Generic ImpEx class to load and export habit list
    """
    def __init__(self, habit_service: HabitService):
        self.habit_service:HabitService = habit_service
        self.logging:logging.Logger = logging.getLogger(__name__)

    def run(self, args):
        """
        Main entry point to the ImpEx client
        :param args
        :return:
        """
        if args.read_from_file:
            return self.read_from_file(args)
        if args.write_to_file:
            return self.write_to_file(args)
        return 0

    def read_from_file(self, args) -> int:
        """
        Read the habit list from a file
        :param args:
        :return:
        :raises Exception: if an error occurred while reading the habit list
        """
        json_string = pathlib.Path(args.read_from_file).read_text(encoding="utf-8")
        habit_list_adapter = TypeAdapter(list[Habit])
        habits = habit_list_adapter.validate_json(json_string)
        print(habits)
        return 0

    def write_to_file(self, args) -> int:
        """
        Write the habit list to a file
        :param args: the command line arguments
        :return:
        :raises Exception: if an error occurred while saving the habit list
        """
        habit_list_adapter = TypeAdapter(list[Habit])
        habits: list[Habit] = self.habit_service.get_all_habits()
        try:
            json_data = habit_list_adapter.dump_json(
            habits,
            indent=2,
            )
        except PydanticSerializationError as e:
            self.logging.error("An error occurred while saving habit list: %s", e)
            return 1
        pathlib.Path(args.write_to_file).write_bytes(json_data)
        return 0
