"""Tests for the models module."""
# Test names serve as docstrings; fixtures intentionally shadow outer names.
# pylint: disable=missing-function-docstring,redefined-outer-name
from datetime import datetime

import pytest

from models.models import Habit, ExecutionFrequency, HabitExecution


def test_habit_instance():
    d: datetime = datetime.now()
    h: Habit = Habit(id=0, name="First Habit", start_date=d, frequency=ExecutionFrequency.DAILY,
                     description="Description")
    assert h.id == 0
    assert h.name == "First Habit"
    assert h.start_date == d
    assert h.frequency == ExecutionFrequency.DAILY
    assert h.description == "Description"


def test_habit_instance_with_executions():
    d: datetime = datetime.now()
    e: HabitExecution = HabitExecution(id=0, habit_id=0, date=d, comment="No comment")
    h: Habit = Habit(id=0, name="First Habit", start_date=d, frequency=ExecutionFrequency.DAILY,
                     description="Description", executions=[e])
    assert h.id == 0
    assert h.name == "First Habit"
    assert h.start_date == d
    assert h.frequency == ExecutionFrequency.DAILY
    assert h.description == "Description"
    assert h.executions == [e]
    assert h.executions[0].habit_id == 0
    assert h.executions[0].date == d


@pytest.mark.xfail()
def test_habit_incomplete_instance():
    d: datetime = datetime.now()
    _ = Habit(id=0, start_date=d, frequency=ExecutionFrequency.DAILY)


def test_habit_no_id_instance():
    d: datetime = datetime.now()
    h: Habit = Habit(name="First Habit", start_date=d, frequency=ExecutionFrequency.DAILY,
                     description="Description")
    assert h.id is None
    assert h.name == "First Habit"
    assert h.start_date == d
    assert h.frequency == ExecutionFrequency.DAILY
    assert h.description == "Description"


def test_habit_frequency_serializes_as_string():
    d: datetime = datetime(2026, 1, 1, 12, 0, 0)
    h: Habit = Habit(name="First Habit", start_date=d, frequency=ExecutionFrequency.DAILY,
                     description="Description")
    assert '"frequency":"daily"' in h.model_dump_json()


def test_habit_invalid_frequency_rejected():
    d: datetime = datetime(2026, 1, 1, 12, 0, 0)
    with pytest.raises(ValueError):
        Habit(name="First Habit", start_date=d, frequency="hourly",
              description="Description")


def test_habit_empty_name_rejected():
    d: datetime = datetime(2026, 1, 1, 12, 0, 0)
    with pytest.raises(ValueError):
        Habit(name="   ", start_date=d, frequency=ExecutionFrequency.DAILY,
              description="Description")
