"""Tests for the habit_service module."""
from datetime import datetime

import pytest

from models.models import Habit, ExecutionFrequency
from repository.json_repository import JsonRepository
from services.habit_service import HabitService


@pytest.fixture
def habit_service(tmp_path) -> HabitService:
    json_file: str = 'tests/habit_service_test.json'
    return JsonRepository(tmp_path.joinpath(json_file))


@pytest.fixture
def simple_habit() -> Habit:
    h: Habit = Habit(id=1, name='Habit 1', description='Habit 1', frequency=ExecutionFrequency.DAILY,
                     start_date=datetime.today())
    return h


def test_add_habit(simple_habit: Habit, habit_service: HabitService) -> None:
    habit_service.add_habit(simple_habit)
