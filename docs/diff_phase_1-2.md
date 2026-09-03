# Differences between Phase 1 (Concept) and Phase 2 (Implementation)

The course schedule foresees tutor feedback between the conception phase and
the development/reflection phase, so some drift between the submitted concept
(`1 Conception Phase.md` / the Phase 1 PDF) and the actual implementation is
expected and intentional. This document lists the differences explicitly, and
the reason for each of them.

## What was implemented as designed

- The strict layering (presentation / service / domain / infrastructure) and
  the separation of the analytics module as a stateless, pure functional
  layer - as drawn in the Phase 1 class and sequence diagrams.
- Plain JSON files as the persistence mechanism (no tool lock-in), the
  Rich library for the user interface, and the datetime module for all
  calendar arithmetic.
- All acceptance criteria from the assignment (5 predefined habits with
  4 weeks of sample data, the four analytics functions, a unit test suite).

## Differences

| # | Phase 1 concept | Phase 2 implementation | Reason |
|---|-----------------|------------------------|--------|
| 1 | A single `JsonHabitRepository` class | `HabitRepository` abstract base class, a `JsonRepository` implementation and a `RepositoryFactory` that selects the implementation from configuration | The concept claimed the repository pattern would make the storage backend swappable; the abstract base class plus factory actually deliver that promise (a future SQLite repository can be added without touching the service) |
| 2 | `analytics` functions named `filter_by_periodicity`, `calculate_longest_streak`, `get_longest_streak_overall`, returning a bare `int` for streaks | `get_all_habits`, `get_habits_by_periodicity`, `get_longest_streak_for_habit`, `get_longest_streak_all`; streaks are returned as a frozen `Streak` dataclass (habit name, start, end, length in periods) | Renamed to state exactly what each function returns; the `Streak` value object lets the UIs show *which* habit and *when*, not just a number. `get_all_habits` was required by the assignment but missing from the Phase 1 diagram |
| 3 | Streak length not further specified | A streak is a run of consecutive periods with at least one execution each: calendar days for daily habits, ISO weeks (Monday-Sunday) for weekly habits; habits without executions have no streak (`None`) | The assignment defines streaks in periods ("14-day streak"), so the implementation is period-based, which also makes daily and weekly habits symmetric |
| 4 | Domain logic lives on the entity: `Habit.execute()` validates rules and mutates state, e.g. preventing duplicate check-offs within the same period | Executing a habit goes through `HabitService.execute_habits` to `JsonRepository.execute_habit`, which appends the execution and persists. Duplicate check-offs within a period are not rejected | Validation that belongs to the data shape (non-empty name, valid frequency) moved into the Pydantic models; workflow logic moved up into the service. Duplicate check-offs are harmless by design: the analytics deduplicate executions per period, so a streak is never inflated |
| 5 | `Habit` and `HabitExecution` are hand-written classes; serialization via Python's built-in `json` module | Domain models are Pydantic `BaseModel`s; a `HabitJsonSerializer` uses Pydantic's `TypeAdapter` to validate on load and dump on save (still plain JSON on disk) | Validation on load gives free type checking of the persisted data; the `json` module plan from Phase 1 is effectively still followed, one level up |
| 6 | Entity ids are `String`; habits carry a `created_at` timestamp | Ids are `int` (assigned by the repository on save, `None` for new objects); the creation timestamp is the `start_date` field | Integer ids are simpler to assign (`max id + 1`) and to type in the UIs; `start_date` doubles as the creation timestamp |
| 7 | Python `>= 3.7` | Python `>= 3.11` | The course asks for modern Python; 3.11 gives `StrEnum`, modern typing syntax (`list[Habit]`) and better error messages |
| 8 | A single `CLI` client class in the presentation layer | Two clients: a `RichTui` interactive menu (9 options) and a non-interactive `CLI` for import/export/delete/analyse flags, glued together in the `habito` package entry point with argparse | The interactive menu serves everyday use, the flag-based client makes the functionality scriptable. The menu also grew during development: deleting a habit and the three analytics views are menu entries now, which Phase 1 did not foresee |
| 9 | `--read-from-file` "replaces the database" (impl_plan.md) | Import appends to the current repository; ids are re-assigned on import so existing habits are never overwritten | Replacing the whole database from a file is destructive; appending with fresh ids makes import safe to repeat |

## Added in Phase 2 (not in the concept)

- Packaging as an installable Python package (`pyproject.toml`) that provides
  the `habito` command.
- Configuration via environment / `.env` file (repository choice, JSON file
  path, logging level) instead of hard-coded values.
- A deterministic sample-data generator (`scripts/generate_sample_data.py`)
  for the 5 predefined habits with 4 weeks of example tracking data.
- A unit test suite (domain models, repository, serializer, factory,
  analytics, service and CLI; 54 tests).