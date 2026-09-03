"""
Testing for the analytics functions
"""
# Test names serve as docstrings; fixtures intentionally shadow outer names.
# pylint: disable=missing-function-docstring,redefined-outer-name
from datetime import date, datetime, timedelta

from models.models import Habit, ExecutionFrequency, HabitExecution
from utils import analytics
from utils.analytics import Streak


def execution(habit_id: int, execution_id: int, day: date,
              comment: str = "done") -> HabitExecution:
    return HabitExecution(id=execution_id, habit_id=habit_id, comment=comment,
                          date=datetime(day.year, day.month, day.day, 8, 0, 0))


def daily_habit(habit_id: int = 1, name: str = "Drink water") -> Habit:
    return Habit(id=habit_id, name=name, description=name,
                 frequency=ExecutionFrequency.DAILY,
                 start_date=datetime(2026, 1, 1))


def weekly_habit(habit_id: int = 1, name: str = "Weekly review") -> Habit:
    return Habit(id=habit_id, name=name, description=name,
                 frequency=ExecutionFrequency.WEEKLY,
                 start_date=datetime(2026, 1, 1))


def test_perfect_daily_run():
    habit = daily_habit()
    habit.executions = [execution(1, i + 1, date(2026, 1, 1) + timedelta(days=i))
                        for i in range(28)]
    streak = analytics.get_longest_streak_for_habit(habit)
    assert streak == Streak(habit_id=1, habit_name="Drink water",
                            frequency=ExecutionFrequency.DAILY,
                            start=date(2026, 1, 1), end=date(2026, 1, 28),
                            length=28)


def test_daily_run_broken_by_gap():
    habit = daily_habit()
    days = ([date(2026, 1, 1) + timedelta(days=i) for i in range(10)]
            + [date(2026, 1, 14) + timedelta(days=i) for i in range(12)])
    habit.executions = [execution(1, i + 1, day) for i, day in enumerate(days)]
    streak = analytics.get_longest_streak_for_habit(habit)
    assert streak.start == date(2026, 1, 14)
    assert streak.end == date(2026, 1, 25)
    assert streak.length == 12


def test_weekly_streak():
    habit = weekly_habit()
    # executions in 6 consecutive ISO weeks (Mondays 2026-01-05 .. 2026-02-09)
    mondays = [date(2026, 1, 5) + timedelta(weeks=i) for i in range(6)]
    habit.executions = [execution(1, i + 1, monday + timedelta(days=2))
                        for i, monday in enumerate(mondays)]
    streak = analytics.get_longest_streak_for_habit(habit)
    assert streak == Streak(habit_id=1, habit_name="Weekly review",
                            frequency=ExecutionFrequency.WEEKLY,
                            start=date(2026, 1, 5), end=date(2026, 2, 9),
                            length=6)


def test_weekly_streak_broken_by_missed_week():
    habit = weekly_habit()
    mondays = [date(2026, 1, 5), date(2026, 1, 12), date(2026, 1, 26),
               date(2026, 2, 2), date(2026, 2, 16)]
    habit.executions = [execution(1, i + 1, monday) for i, monday in enumerate(mondays)]
    streak = analytics.get_longest_streak_for_habit(habit)
    assert streak.length == 2
    # two runs of length 2 exist; ties are broken by the earliest start
    assert streak.start == date(2026, 1, 5)


def test_weekly_streak_across_iso_year_boundary():
    habit = weekly_habit()
    # ISO week 53 of 2026 starts Monday 2026-12-28; week 1 of 2027 starts 2027-01-04
    mondays = [date(2026, 12, 14), date(2026, 12, 21), date(2026, 12, 28),
               date(2027, 1, 4), date(2027, 1, 11)]
    habit.executions = [execution(1, i + 1, monday) for i, monday in enumerate(mondays)]
    streak = analytics.get_longest_streak_for_habit(habit)
    assert streak == Streak(habit_id=1, habit_name="Weekly review",
                            frequency=ExecutionFrequency.WEEKLY,
                            start=date(2026, 12, 14), end=date(2027, 1, 11),
                            length=5)


def test_single_execution_streak():
    habit = daily_habit()
    habit.executions = [execution(1, 1, date(2026, 3, 1))]
    streak = analytics.get_longest_streak_for_habit(habit)
    assert streak is not None
    assert streak.length == 1
    assert streak.start == streak.end == date(2026, 3, 1)


def test_no_executions_returns_none():
    assert analytics.get_longest_streak_for_habit(daily_habit()) is None
    assert analytics.get_longest_streak_all([daily_habit(), weekly_habit()]) is None


def test_get_all_habits():
    habits = [daily_habit(1), daily_habit(2)]
    assert analytics.get_all_habits(habits) == habits


def test_get_habits_by_periodicity():
    daily = daily_habit(1)
    weekly = weekly_habit(2)
    habits = [daily, weekly]
    assert analytics.get_habits_by_periodicity(habits, ExecutionFrequency.DAILY) == [daily]
    assert analytics.get_habits_by_periodicity(habits, ExecutionFrequency.WEEKLY) == [weekly]
    assert analytics.get_habits_by_periodicity(habits, ExecutionFrequency("daily")) == [daily]


def test_longest_streak_all_picks_longest():
    strong = daily_habit(1, "Strong habit")
    strong.executions = [execution(1, i + 1, date(2026, 1, 1) + timedelta(days=i))
                         for i in range(10)]
    weak = daily_habit(2, "Weak habit")
    weak.executions = [execution(2, 1, date(2026, 1, 1)),
                       execution(2, 2, date(2026, 1, 3))]
    streak = analytics.get_longest_streak_all([weak, strong])
    assert streak is not None
    assert streak.habit_id == 1
    assert streak.length == 10


def test_longest_streak_all_tie_broken_by_earliest_start():
    first = daily_habit(1, "First")
    first.executions = [execution(1, i + 1, date(2026, 1, 1) + timedelta(days=i))
                        for i in range(3)]
    second = daily_habit(2, "Second")
    second.executions = [execution(2, i + 1, date(2026, 2, 1) + timedelta(days=i))
                         for i in range(3)]
    streak = analytics.get_longest_streak_all([second, first])
    assert streak is not None
    assert streak.habit_id == 1


def test_analytics_does_not_mutate_input():
    habit = daily_habit()
    days = [date(2026, 1, 5) + timedelta(days=i) for i in range(5)]
    habit.executions = [execution(1, i + 1, day) for i, day in enumerate(days)]
    original_order = list(habit.executions)
    analytics.get_longest_streak_for_habit(habit)
    analytics.get_longest_streak_all([habit])
    assert habit.executions == original_order
