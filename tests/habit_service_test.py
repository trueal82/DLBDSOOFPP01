"""Tests for the habit_service module."""
# Test names serve as docstrings; fixtures intentionally shadow outer names.
# pylint: disable=missing-function-docstring,redefined-outer-name
from datetime import date, timedelta

import pytest

from models.models import ExecutionFrequency
from repository.json_repository import JsonRepository
from services.habit_service import HabitService


@pytest.fixture
def habit_service(tmp_path) -> HabitService:
    return HabitService(repository=JsonRepository(str(tmp_path / "habit_service_test.json")))


def test_add_habit_round_trip(habit_service: HabitService) -> None:
    habit = habit_service.add_habit("Habit 1", "daily", "Some description")
    assert habit.id is not None
    loaded = habit_service.get_habit_by_id(habit.id)
    assert loaded.name == "Habit 1"
    assert loaded.frequency == ExecutionFrequency.DAILY


def test_add_habit_invalid_frequency(habit_service: HabitService) -> None:
    with pytest.raises(ValueError):
        habit_service.add_habit("Habit 1", "hourly")


def test_add_habit_empty_name(habit_service: HabitService) -> None:
    with pytest.raises(ValueError):
        habit_service.add_habit("", "daily")


def test_delete_habit(habit_service: HabitService) -> None:
    habit = habit_service.add_habit("Habit 1", "daily")
    habit_service.delete_habit(habit.id)
    with pytest.raises(ValueError):
        habit_service.get_habit_by_id(habit.id)


def test_delete_missing_habit_raises(habit_service: HabitService) -> None:
    with pytest.raises(ValueError):
        habit_service.delete_habit(999)


def test_execute_persists_execution(habit_service: HabitService) -> None:
    habit = habit_service.add_habit("Habit 1", "daily")
    habit_service.execute_habits(habit.id, "felt good")
    reloaded = HabitService(repository=JsonRepository(habit_service.repository.json_file_path))
    stored = reloaded.get_habit_by_id(habit.id)
    assert len(stored.executions) == 1
    assert stored.executions[0].comment == "felt good"


def test_get_due_habits_daily(habit_service: HabitService) -> None:
    habit = habit_service.add_habit("Habit 1", "daily")
    habit_service.execute_habits(habit.id, "today")
    today = date.today()
    assert habit_service.get_due_habits(today) == []
    assert habit_service.get_due_habits(today + timedelta(days=1)) != []


def test_get_due_habits_weekly(habit_service: HabitService) -> None:
    habit = habit_service.add_habit("Habit 2", "weekly")
    habit_service.execute_habits(habit.id, "this week")
    today = date.today()
    assert habit_service.get_due_habits(today) == []
    assert habit_service.get_due_habits(today + timedelta(weeks=1)) != []


def test_analytics_delegates(habit_service: HabitService) -> None:
    habit = habit_service.add_habit("Habit 1", "daily")
    assert habit_service.get_habits_by_periodicity("daily") == [habit]
    assert habit_service.get_habits_by_periodicity("weekly") == []
    assert habit_service.get_longest_streak_all() is None
    assert habit_service.get_longest_streak_for_habit(habit.id) is None
    with pytest.raises(ValueError):
        habit_service.get_habits_by_periodicity("hourly")
