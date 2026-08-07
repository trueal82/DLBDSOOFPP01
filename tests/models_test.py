"""Tests for the models module."""
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
    h: Habit = Habit(id=0, start_date=d, frequency=ExecutionFrequency.DAILY)


def test_habit_no_id_instance():
    d: datetime = datetime.now()
    h: Habit = Habit(name="First Habit", start_date=d, frequency=ExecutionFrequency.DAILY,
                     description="Description")
    assert h.id == ""
    assert h.name == "First Habit"
    assert h.start_date == d
    assert h.frequency == ExecutionFrequency.DAILY
    assert h.description == "Description"
