"""
A strictly functional module to work on Habits
"""
from typing import Tuple
from datetime import date, timedelta
from models.models import Habit, HabitExecution


def get_all_habits(habits: list[Habit]) -> list[str]:
    """
    Returns a list of all habits
    """
    l = []
    for habit in habits:
        l.append(habit.toString())
    return l


def longest_streak(habit: Habit) -> Tuple[date, date, int]:
    """Returns the longest streak from the list of streaks."""
    executions: list[HabitExecution] = habit.executions
    executions.sort(key=lambda x: x.date)
    longest_so_far_from: date = None
    longest_so_far_to: date = None
    last_execution = None
    this_streak_from: date = None
    this_streak_to: date = None
    for execution in executions:
        if not last_execution:
            # First execution, setting up this streak counter
            last_execution = execution.date.date()
            this_streak_from = execution.date.date()
            this_streak_to = execution.date.date()
            longest_so_far_from = execution.date.date()
            longest_so_far_to = execution.date.date()
        else:
            if execution.date - timedelta(days= int(habit.frequency.value)) > last_execution:
                # we broke the streak
                # check if this streak is longer than the longest
                if this_streak_from - this_streak_to > longest_so_far_from - longest_so_far_to:
                    # this is longer
                    longest_so_far_to = this_streak_to
                    longest_so_far_from = this_streak_to
                else:
                    # it is shorter
                    # in any case reset this_streak
                    this_streak_from = execution.date.date()
                    this_streak_to = execution.date.date()
            else:
                # streak continues
                this_streak_to = execution.date.date()

    return (
        longest_so_far_from,
        longest_so_far_to,
        (longest_so_far_to-longest_so_far_from).days
    )
