"""Tests for the command line client."""
# Test names serve as docstrings; fixtures intentionally shadow outer names.
# pylint: disable=missing-function-docstring,redefined-outer-name
import argparse
import json
from datetime import datetime

import pytest

from clients.cli import CLI
from repository.json_repository import JsonRepository
from services.habit_service import HabitService
from utils.habit_json_serializer import HabitJsonSerializer


@pytest.fixture
def service(tmp_path) -> HabitService:
    return HabitService(repository=JsonRepository(str(tmp_path / "repo.json")))


@pytest.fixture
def cli(service: HabitService) -> CLI:
    return CLI(service)


def args(**kwargs) -> argparse.Namespace:
    defaults = {"read_from_file": None, "write_to_file": None,
                "delete_habit": None, "analyse": False}
    defaults.update(kwargs)
    return argparse.Namespace(**defaults)


def test_write_then_read_round_trip(cli: CLI, service: HabitService, tmp_path) -> None:
    service.add_habit("Habit 1", "daily", "Description")
    export = str(tmp_path / "export.json")
    assert cli.run(args(write_to_file=export)) == 0
    imported = HabitJsonSerializer().read_from_file(export)
    assert len(imported) == 1
    assert imported[0].name == "Habit 1"


def test_read_from_file_merges_with_new_ids(cli: CLI, service: HabitService,
                                            tmp_path) -> None:
    service.add_habit("Existing", "daily", "")
    import_file = tmp_path / "import.json"
    import_file.write_text(
        json.dumps([{"id": 7, "name": "Imported", "description": "Desc",
                     "frequency": "weekly", "start_date": "2026-01-01T08:00:00",
                     "executions": [{"id": 1, "habit_id": 7,
                                     "date": "2026-01-05T08:00:00",
                                     "comment": "done"}]}]),
        encoding="utf-8")
    assert cli.run(args(read_from_file=str(import_file))) == 0
    habits = service.get_all_habits()
    assert [habit.name for habit in habits] == ["Existing", "Imported"]
    imported = habits[1]
    assert imported.id == 2  # ids are re-assigned, not taken from the file
    assert len(imported.executions) == 1


def test_read_from_missing_file_fails_cleanly(cli: CLI, tmp_path) -> None:
    assert cli.run(args(read_from_file=str(tmp_path / "nope.json"))) == 1


def test_delete_habit(cli: CLI, service: HabitService) -> None:
    habit = service.add_habit("Habit 1", "daily")
    assert cli.run(args(delete_habit=habit.id)) == 0
    assert service.get_all_habits() == []


def test_delete_missing_habit_fails_cleanly(cli: CLI) -> None:
    assert cli.run(args(delete_habit=999)) == 1


def test_analyse_runs_with_empty_repository(cli: CLI, capsys) -> None:
    assert cli.run(args(analyse=True)) == 0
    assert "Currently tracked habits: 0" in capsys.readouterr().out


def test_analyse_prints_streaks(cli: CLI, service: HabitService, capsys) -> None:
    habit = service.add_habit("Habit 1", "daily", start_date=datetime(2026, 1, 1))
    service.execute_habits(habit.id, "done")
    assert cli.run(args(analyse=True)) == 0
    output = capsys.readouterr().out
    assert "Habit 1" in output
    assert "1 period(s)" in output


def test_no_options_is_a_no_op(cli: CLI) -> None:
    assert cli.run(args()) == 0
