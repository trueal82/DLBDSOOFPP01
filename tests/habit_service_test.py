"""Tests for the habit_service module."""
import pytest
from datetime import datetime
from datetime import datetime
from habit_service import HabitService
from models import Habit, ExecutionFrequency, HabitExecution
from repository.json_repository import JsonRepository


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
