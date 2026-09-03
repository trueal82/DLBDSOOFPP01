"""Tests for the repository factory."""
# Test names serve as docstrings; fixtures intentionally shadow outer names.
# pylint: disable=missing-function-docstring,redefined-outer-name
import pytest

from repository.json_repository import JsonRepository
from repository.repo_factory import RepositoryFactory
from services.habit_service import HabitService


def test_default_repository(monkeypatch) -> None:
    monkeypatch.setattr("config.HABIT_REPOSITORY", "JsonRepository")
    assert isinstance(RepositoryFactory.get_repository(), JsonRepository)


def test_unknown_repository_type_raises() -> None:
    with pytest.raises(ValueError):
        RepositoryFactory.get_repository("NonexistentRepository")


def test_unset_repository_type_raises(monkeypatch) -> None:
    monkeypatch.setattr("config.HABIT_REPOSITORY", "")
    with pytest.raises(ValueError):
        RepositoryFactory.get_repository()


def test_service_with_explicit_repository_type(monkeypatch, tmp_path) -> None:
    monkeypatch.setattr("config.JSON_FILE_PATH", str(tmp_path / "repo.json"))
    service = HabitService("JsonRepository")
    assert service.repository.json_file_path == str(tmp_path / "repo.json")


def test_service_without_arguments(monkeypatch, tmp_path) -> None:
    monkeypatch.setattr("config.JSON_FILE_PATH", str(tmp_path / "repo.json"))
    service = HabitService()
    assert service.get_all_habits() == []
