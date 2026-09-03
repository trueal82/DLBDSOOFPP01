"""Tests for the HabitJsonSerializer."""
# Test names serve as docstrings; fixtures intentionally shadow outer names.
# pylint: disable=missing-function-docstring,redefined-outer-name
from datetime import datetime

import pytest

from models.models import ExecutionFrequency, Habit
from utils.habit_json_serializer import HabitJsonSerializer


@pytest.fixture
def serializer() -> HabitJsonSerializer:
    return HabitJsonSerializer()


@pytest.fixture
def habit() -> Habit:
    return Habit(id=1, name="Habit 1", description="Description",
                 frequency=ExecutionFrequency.WEEKLY,
                 start_date=datetime(2026, 1, 1, 8, 0, 0))


def test_round_trip(serializer: HabitJsonSerializer, tmp_path, habit: Habit) -> None:
    filename = str(tmp_path / "habits.json")
    serializer.write_to_file(filename, [habit])
    loaded = serializer.read_from_file(filename)
    assert loaded == [habit]
    assert loaded[0].frequency == ExecutionFrequency.WEEKLY


def test_read_missing_file_returns_empty_list(serializer: HabitJsonSerializer,
                                              tmp_path) -> None:
    assert serializer.read_from_file(str(tmp_path / "does_not_exist.json")) == []


def test_read_malformed_file_raises(serializer: HabitJsonSerializer, tmp_path) -> None:
    filename = tmp_path / "broken.json"
    filename.write_text("{not json", encoding="utf-8")
    with pytest.raises(ValueError):
        serializer.read_from_file(str(filename))


def test_write_creates_missing_directories(serializer: HabitJsonSerializer,
                                           tmp_path, habit: Habit) -> None:
    filename = str(tmp_path / "sub" / "dir" / "habits.json")
    serializer.write_to_file(filename, [habit])
    assert serializer.read_from_file(filename) == [habit]
