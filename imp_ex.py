import logging

from habit_json_serializer import HabitJsonSerializer


class ImpEx:
    def __init__(self):
        self.logging: logging.Logger = logging.getLogger(__name__)
        self.serializer: HabitJsonSerializer = HabitJsonSerializer()

    def run(self, args):
        """
        Main entry point to the ImpEx client
        :param args
        :return:
        """
        if args.read_from_file:
            return self.serializer.read_from_file(args.read_from_file)
        if args.write_to_file:
            return self.serializer.write_to_file(args.write_to_file)
        return 0
