"""
Command line client for import/export, deleting and analysing habits.
"""
import logging
import pathlib

from models.models import Habit, HabitExecution
from services.habit_service import HabitService
from utils.habit_json_serializer import HabitJsonSerializer


class CLI:
    """A non-interactive command line client for habit import/export,
    deletion and analysis."""

    def __init__(self, service: HabitService):
        self.service: HabitService = service
        self.logging: logging.Logger = logging.getLogger(__name__)
        self.serializer: HabitJsonSerializer = HabitJsonSerializer()

    def run(self, args) -> int:
        """
        Main entry point to the ImpEx client
        :param args: parsed command line arguments
        :return: 0 on success, 1 on error
        """
        if args.read_from_file:
            return self.read_from_file(args.read_from_file)
        if args.write_to_file:
            return self.write_to_file(args.write_to_file)
        if args.delete_habit is not None:
            return self.delete_habit(args.delete_habit)
        if args.analyse:
            return self.analyse()
        return 0

    def read_from_file(self, filename: str) -> int:
        """Reads habits (with their executions) from a json file and adds
        them to the current repository. Ids are re-assigned on import so
        existing habits are never overwritten."""
        try:
            if not pathlib.Path(filename).exists():
                raise FileNotFoundError(f"no such file: {filename}")
            habits: list[Habit] = self.serializer.read_from_file(filename)
            for habit in habits:
                imported: Habit = self.service.add_habit(
                    name=habit.name, frequency=habit.frequency.value,
                    description=habit.description,
                    start_date=habit.start_date)
                # re-attach the imported executions with fresh ids
                imported.executions = [
                    HabitExecution(id=number, habit_id=imported.id,
                                   date=execution.date, comment=execution.comment)
                    for number, execution in enumerate(habit.executions, start=1)]
                self.service.update_habit(imported)
        except (OSError, ValueError) as e:
            self.logging.error("Could not import habits from %s: %s", filename, e)
            return 1
        self.logging.info("Imported %d habit(s) from %s", len(habits), filename)
        return 0

    def write_to_file(self, filename: str) -> int:
        """Writes all habits (with their executions) to a json file."""
        try:
            habits: list[Habit] = self.service.get_all_habits()
            self.serializer.write_to_file(filename=filename, habits=habits)
        except (OSError, ValueError) as e:
            self.logging.error("Could not export habits to %s: %s", filename, e)
            return 1
        self.logging.info("Exported %d habit(s) to %s", len(habits), filename)
        return 0

    def delete_habit(self, habit_id: int) -> int:
        """Deletes the habit with the given id."""
        try:
            habit: Habit = self.service.get_habit_by_id(habit_id)
        except ValueError as e:
            self.logging.error(str(e))
            return 1
        self.service.delete_habit(habit_id)
        self.logging.info("Deleted habit '%s' (id %d)", habit.name, habit_id)
        return 0

    def analyse(self) -> int:
        """Prints the four required analytics results."""
        habits: list[Habit] = self.service.get_all_habits()
        print(f"Currently tracked habits: {len(habits)}")
        for frequency in self.service.get_execution_frequencies():
            matching = self.service.get_habits_by_periodicity(frequency)
            print(f"  {frequency} habits: {[h.name for h in matching]}")
        longest_all = self.service.get_longest_streak_all()
        if longest_all is None:
            print("No habit was ever executed - no streaks yet.")
            return 0
        print(f"Longest streak of all habits: "
              f"{longest_all.habit_name} with {longest_all.length} period(s) "
              f"({longest_all.start} to {longest_all.end})")
        for habit in habits:
            streak = self.service.get_longest_streak_for_habit(habit.id)
            if streak is None:
                print(f"  {habit.name}: no executions yet")
            else:
                print(f"  {habit.name}: {streak.length} period(s) "
                      f"({streak.start} to {streak.end})")
        return 0
