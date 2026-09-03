# Habito
This is the implementation of Habito





# Installation
The application is an installable Python package. The recommended way is a
virtual environment:

```shell
# Create a .venv
$ python -m venv .venv
# Activate the .venv
$ source .venv/bin/activate
# Install the application (this also installs all dependencies)
$ pip install .
```

That's it - the `habito` command is now available.

To work on the code instead of just using it, install it in editable mode
(includes the development dependencies like pytest and pylint):

```shell
$ pip install -e '.[dev]'
```

This way changes to the source take effect immediately, without reinstalling.
All commands below work the same way in this setup.

## Running the application
The easiest way is to just run the *`habito`* command - this starts the
interactive menu (TUI), which lets you show, add, execute, delete and
analyse habits.

All functionality is also available as non-interactive command line flags:

```shell
# Export all habits (and their executions) to a json file
$ habito --write-to-file backup.json

# Import habits (and their executions) from a json file
$ habito --read-from-file backup.json

# Delete the habit with the given id
$ habito --delete-habit 2

# Print the analytics summary (all habits, by periodicity, longest streaks)
$ habito --analyse
```

Inside the repository everything also works without installing:
*`python3 main.py`* starts the TUI with the same behaviour.

> **Note on where your data lives:** the tracker stores its data in
> `./data/repository.json` *relative to the directory you start it from*
> (see Configuration below). Start it from the project directory to use the
> shipped sample data, or point `JSON_FILE_PATH` in your `.env` to an
> absolute path to use one data file from anywhere.

## Configuration
Configuration is read from the environment (a `.env` file is supported, see
`template.env`):

| Variable           | Default                  | Meaning                                    |
|--------------------|--------------------------|--------------------------------------------|
| `HABIT_REPOSITORY` | `JsonRepository`         | Repository implementation to use            |
| `JSON_FILE_PATH`   | `./data/repository.json` | File the JsonRepository persists to         |
| `LOG_LEVEL`        | `INFO`                   | Logging level                               |

## Predefined habits and sample data
The application ships with **5 predefined habits** (3 daily, 2 weekly) and
**4 weeks of example tracking data** each, stored in
`data/repository.json` (the default repository file). Running the application
therefore already shows populated analytics - the longest overall streak is
"Drink water" with 28 consecutive days.

To start fresh, point `JSON_FILE_PATH` in your `.env` to another file (e.g.
`./data/my.json`), or delete `data/repository.json` - a missing file is
treated as an empty repository.

New habits are created via the TUI (menu option *Add habit*) - you are asked
for a name, an optional description and the frequency (`daily` or `weekly`).
A task is completed within its period via *Mark habit done*: a daily habit
must be checked off once per calendar day, a weekly habit once per ISO week
(Monday-Sunday); missing a period breaks the streak.

The sample data can be regenerated deterministically at any time:

```shell
$ python scripts/generate_sample_data.py
```

## Analytics
The analytics module (`utils/analytics.py`) is implemented in the functional
programming paradigm and provides the four required functions:

1. `get_all_habits(habits)` - list of all currently tracked habits
2. `get_habits_by_periodicity(habits, frequency)` - all habits with the same periodicity
3. `get_longest_streak_all(habits)` - the longest run streak of all defined habits
4. `get_longest_streak_for_habit(habit)` - the longest run streak of a given habit

A streak is a run of consecutive periods (calendar days for daily habits,
ISO weeks for weekly habits) with at least one execution each; its length is
the number of periods in the run.

## Running the test suite
```shell
$ pip install -e '.[dev]'
$ python -m pytest
```

The suite covers the domain models, the repository, the analytics module, the
service layer and the command line client.