"""Tests for the JsonRepository."""
# Test names serve as docstrings; fixtures intentionally shadow outer names.
# pylint: disable=missing-function-docstring,redefined-outer-name
import json
import os
from datetime import date, datetime

import pytest

from models.models import ExecutionFrequency, Habit, HabitExecution
from repository.json_repository import JsonRepository


@pytest.fixture
def repo(tmp_path) -> JsonRepository:
    return JsonRepository(str(tmp_path / "repo.json"))


def test_load_round_trip_with_string_frequencies(tmp_path) -> None:
    """Regression test: the persisted frequency strings ('daily'/'weekly')
    must load back into the enum."""
    filename = str(tmp_path / "repo.json")
    data = [{"id": 1, "name": "Habit 1", "description": "Desc",
             "frequency": "daily", "start_date": "2026-01-01T08:00:00",
             "executions": []},
            {"id": 2, "name": "Habit 2", "description": "Desc",
             "frequency": "weekly", "start_date": "2026-01-01T08:00:00",
             "executions": []}]
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file)
    repo = JsonRepository(filename)
    assert [habit.frequency for habit in repo.get_all_habits()] == [
        ExecutionFrequency.DAILY, ExecutionFrequency.WEEKLY]


def test_missing_file_starts_empty(repo: JsonRepository) -> None:
    assert repo.get_all_habits() == []


def test_add_assigns_incrementing_ids(repo: JsonRepository) -> None:
    first = repo.add_habit(_habit("First"))
    second = repo.add_habit(_habit("Second"))
    assert (first.id, second.id) == (1, 2)
    reloaded = JsonRepository(repo.json_file_path)
    assert [habit.id for habit in reloaded.get_all_habits()] == [1, 2]


def _habit(name: str) -> Habit:
    return Habit(name=name, description=name,
                 frequency=ExecutionFrequency.DAILY,
                 start_date=datetime(2026, 1, 1))


def test_delete_habit(repo: JsonRepository) -> None:
    habit = repo.add_habit(_habit("First"))
    repo.delete_habit(habit.id)
    assert repo.get_all_habits() == []
    with pytest.raises(ValueError):
        repo.delete_habit(habit.id)


def test_delete_missing_habit_does_not_rewrite_file(repo: JsonRepository) -> None:
    filename = repo.json_file_path
    with pytest.raises(ValueError):
        repo.delete_habit(999)
    assert not os.path.exists(filename)


def test_get_next_free_id(repo: JsonRepository) -> None:
    assert repo.get_next_free_id() == 1
    repo.add_habit(_habit("First"))
    repo.add_habit(_habit("Second"))
    assert repo.get_next_free_id() == 3


def test_get_due_habits_daily_across_month_boundary(repo: JsonRepository) -> None:
    habit = repo.add_habit(_habit("First"))
    habit.executions.append(HabitExecution(id=1, habit_id=habit.id,
                                           date=datetime(2026, 1, 31, 18, 0, 0),
                                           comment="done"))
    repo.update_habit(habit)
    # last execution was Jan 31; on Feb 2 the daily habit is due again
    assert repo.get_due_habits(date(2026, 1, 31)) == []
    assert repo.get_due_habits(date(2026, 2, 2)) == [habit]


def test_get_due_habits_weekly_within_and_across_week(repo: JsonRepository) -> None:
    habit = repo.add_habit(Habit(name="Weekly", description="",
                                 frequency=ExecutionFrequency.WEEKLY,
                                 start_date=datetime(2026, 1, 5)))
    habit.executions.append(HabitExecution(id=1, habit_id=habit.id,
                                           date=datetime(2026, 1, 5, 18, 0, 0),
                                           comment="done"))
    repo.update_habit(habit)
    assert repo.get_due_habits(date(2026, 1, 10)) == []
    assert repo.get_due_habits(date(2026, 1, 12)) == [habit]


def test_get_due_habits_never_executed(repo: JsonRepository) -> None:
    habit = repo.add_habit(_habit("First"))
    assert repo.get_due_habits(date(2026, 1, 1)) == [habit]


def test_execute_habit_assigns_execution_ids(repo: JsonRepository) -> None:
    habit = repo.add_habit(_habit("First"))
    repo.execute_habit(habit.id, "first")
    repo.execute_habit(habit.id, "second")
    stored = repo.get_habit_by_id(habit.id)
    assert [execution.id for execution in stored.executions] == [1, 2]
