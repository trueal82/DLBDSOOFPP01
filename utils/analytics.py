"""
A strictly functional module to work on Habits.

All functions are pure: they never mutate the habits they receive.

Streak semantics
----------------
A habit defines a *period* in which the task must be completed at least
once: one calendar day for daily habits, one ISO week (Monday-Sunday) for
weekly habits. A *streak* is a run of consecutive periods each containing
at least one execution; its length is the number of periods in the run
(a weekly habit done in 4 consecutive weeks has a streak of 4).

Habits without any execution have no streak at all - the streak functions
return ``None`` for them instead of a zero-length streak.
"""
from dataclasses import dataclass
from datetime import date, timedelta
from itertools import groupby

from models.models import ExecutionFrequency, Habit


@dataclass(frozen=True)
class Streak:
    """The longest streak of a habit, expressed in consecutive periods."""
    habit_id: int
    habit_name: str
    frequency: ExecutionFrequency
    start: date  # first day of the first period in the streak
    end: date  # first day of the last period in the streak
    length: int  # number of consecutive periods


def get_all_habits(habits: list[Habit]) -> list[Habit]:
    """
    Returns a list of all currently tracked habits.

    :param habits: all known habits
    :return: the habits, in their original order
    """
    return list(habits)


def get_habits_by_periodicity(habits: list[Habit],
                              frequency: ExecutionFrequency) -> list[Habit]:
    """
    Returns all habits with the given periodicity.

    :param habits: all known habits
    :param frequency: the periodicity to filter for
    :return: the matching habits, in their original order
    """
    return list(filter(lambda habit: habit.frequency == frequency, habits))


def get_longest_streak_for_habit(habit: Habit) -> Streak | None:
    """
    Returns the longest run streak of the given habit.

    :param habit: the habit to analyse
    :return: the longest streak, or None if the habit was never executed
    """
    periods = _periods(habit)
    if not periods:
        return None
    step_days = 1 if habit.frequency == ExecutionFrequency.DAILY else 7
    runs = _consecutive_runs(periods, step_days)
    return _best(map(lambda run: _to_streak(habit, run), runs))


def get_longest_streak_all(habits: list[Habit]) -> Streak | None:
    """
    Returns the longest run streak of all defined habits.

    :param habits: all known habits
    :return: the longest streak, or None if no habit was ever executed
    """
    streaks = filter(None, map(get_longest_streak_for_habit, habits))
    return _best(streaks)


def _iso_week_monday(execution) -> date:
    """Returns the Monday of the ISO week containing the execution's date."""
    return date.fromisocalendar(*execution.date.isocalendar()[:2], 1)


def _periods(habit: Habit) -> list[date]:
    """Returns the sorted, unique start dates of all periods that contain
    at least one execution: calendar days for daily habits, ISO-week
    Mondays for weekly habits."""
    if habit.frequency == ExecutionFrequency.WEEKLY:
        return sorted({_iso_week_monday(execution)
                       for execution in habit.executions})
    return sorted({execution.date.date() for execution in habit.executions})


def _consecutive_runs(periods: list[date],
                      step_days: int) -> list[tuple[date, date, int]]:
    """Groups a sorted list of period anchors into runs of consecutive
    periods. Two anchors are consecutive if they are step_days apart.
    Returns (first, last, length) tuples."""
    grouped = groupby(enumerate(periods),
                      key=lambda ip: ip[1] - timedelta(days=step_days * ip[0]))
    runs = [list(group) for _, group in grouped]
    return [(run[0][1], run[-1][1], len(run)) for run in runs]


def _to_streak(habit: Habit, run: tuple[date, date, int]) -> Streak:
    """Builds a Streak for a habit from a (first, last, length) run."""
    first, last, length = run
    return Streak(habit_id=habit.id, habit_name=habit.name,
                  frequency=habit.frequency, start=first, end=last,
                  length=length)


def _best(streaks) -> Streak | None:
    """Returns the longest of the given streaks; ties are broken by the
    earliest start."""
    candidates = list(streaks)
    if not candidates:
        return None
    return max(candidates, key=lambda streak: (streak.length,
                                               -streak.start.toordinal()))
