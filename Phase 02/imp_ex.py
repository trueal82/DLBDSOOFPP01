import pathlib

from pydantic import TypeAdapter
from models import Habit

from habit_service import HabitService


class ImpEx():
    def __init__(self, habit_service: HabitService):
        self.habit_service:HabitService = habit_service

    def run(self, args):
        """
        Main entry point to the ImpEx client
        :param args
        :return:
        """
        if args.read_from_file:
            self.read_from_file(args)
        elif args.write_to_file:
            self.write_to_file(args)

    def read_from_file(self, args):
        json_string = pathlib.Path(args.read_from_file).read_text()
        habit_list_adapter = TypeAdapter(list[Habit])
        habits = habit_list_adapter.validate_json(json_string)
        print(habits)

    def write_to_file(self, args):
        habit_list_adapter = TypeAdapter(list[Habit])
        habits: list[Habit] = self.habit_service.get_all_habits()
        json_data = habit_list_adapter.dump_json(
            habits,
            indent=2,
        )
        pathlib.Path(args.write_to_file).write_bytes(json_data)


