import logging

from models.models import Habit
from services.habit_service import HabitService
from utils.habit_json_serializer import HabitJsonSerializer


class ImpEx:
    def __init__(self, service: HabitService):
        self.service: HabitService = service
        self.logging: logging.Logger = logging.getLogger(__name__)
        self.serializer: HabitJsonSerializer = HabitJsonSerializer()

    def run(self, args):
        """
        Main entry point to the ImpEx client
        :param args
        :return:
        """
        if args.read_from_file:
            self.serializer.read_from_file(args.read_from_file)
            return 0
        if args.write_to_file:
            try:
                habits: list[Habit] = self.service.get_all_habits()
                self.serializer.write_to_file(filename=args.write_to_file, habits=habits)
            except Exception as e:
                return -1
            return 0
        return 0
