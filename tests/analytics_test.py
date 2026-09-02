"""
Testing for the analytics functions
"""
from datetime import datetime, timedelta

import pytest

from models.models import Habit, ExecutionFrequency, HabitExecution
from utils import analytics


@pytest.fixture
def simple_incremental_case() -> Habit:
    h = Habit(id=1, description="First Habit", name="First Habit", frequency=ExecutionFrequency.DAILY,
              start_date=datetime.today().date() - timedelta(days=7))
    h.executions.append(HabitExecution(id=1, habit_id=1, comment="First Execution",
                                       date=datetime.today().date() - timedelta(days=7)))
    h.executions.append(HabitExecution(id=2, habit_id=1, comment="Second Execution",
                                       date=datetime.today().date() - timedelta(days=6)))
    h.executions.append(HabitExecution(id=3, habit_id=1, comment="Third Execution",
                                       date=datetime.today().date() - timedelta(days=5)))
    h.executions.append(HabitExecution(id=4, habit_id=1, comment="Fourth Execution",
                                       date=datetime.today().date() - timedelta(days=4)))
    h.executions.append(HabitExecution(id=5, habit_id=1, comment="Fifth Execution",
                                       date=datetime.today().date() - timedelta(days=3)))
    h.executions.append(HabitExecution(id=6, habit_id=1, comment="Sixth Execution",
                                       date=datetime.today().date() - timedelta(days=2)))
    h.executions.append(HabitExecution(id=6, habit_id=1, comment="Seventh Execution",
                                       date=datetime.today().date() - timedelta(days=1)))
    h.executions.append(HabitExecution(id=7, habit_id=1, comment="Eighth Execution",
                                       date=datetime.today().date()))

    return h


def test_simple_incremental_case(simple_incremental_case: Habit) -> None:
    assert analytics.longest_streak(simple_incremental_case) == (datetime.today() - timedelta(days=7),
                                                                 datetime.today(),
                                                                 (datetime.today() - timedelta(days=7)) - datetime.today())
