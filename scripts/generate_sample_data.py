"""
Generates the predefined sample data shipped with the application:
5 habits (3 daily, 2 weekly) with 4 weeks of example tracking data each.

The output is deterministic (fixed date range) so it can be regenerated
at any time. Run:

    python scripts/generate_sample_data.py [--output data/repository.json]

The generated data is intentionally non-trivial so the analytics functions
have something interesting to show:

    id  habit              frequency  pattern                       longest streak
    --  -----------------  ---------  ----------------------------  --------------
    1   Drink water        daily      executed every day            28
    2   Read 30 minutes    daily      10-day run, gap, 12-day run   12
    3   Weekly review      weekly     executed every week           4
    4   Gym session        weekly     week on, week off             1
    5   Learn Analysis 1   daily      sparse, irregular             1
"""
import argparse
import sys
from datetime import date, datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

# pylint: disable=wrong-import-position
from models.models import ExecutionFrequency, Habit, HabitExecution
from utils.habit_json_serializer import HabitJsonSerializer
# pylint: enable=wrong-import-position

START_DATE: date = date(2026, 8, 3)  # a Monday; data covers 4 weeks from here


def execution(habit_id: int, execution_id: int, day: date,
              comment: str) -> HabitExecution:
    """Builds an execution at a fixed time of day on the given date."""
    return HabitExecution(id=execution_id, habit_id=habit_id,
                          date=datetime(day.year, day.month, day.day, 18, 0, 0),
                          comment=comment)


def build_habits() -> list[Habit]:
    """Builds the 5 predefined habits with 4 weeks of example data."""
    days = [START_DATE + timedelta(days=offset) for offset in range(28)]
    weeks = days[::7]
    start = datetime.combine(days[0], datetime.min.time())

    water = Habit(id=1, name="Drink water", description="Drink 2 litres of water",
                  frequency=ExecutionFrequency.DAILY, start_date=start)
    water.executions = [execution(1, i + 1, day, "stayed hydrated")
                        for i, day in enumerate(days)]

    reading = Habit(id=2, name="Read 30 minutes",
                    description="Read a book for 30 minutes",
                    frequency=ExecutionFrequency.DAILY, start_date=start)
    reading_days = days[:10] + days[13:25]
    reading.executions = [execution(2, i + 1, day, "read")
                          for i, day in enumerate(reading_days)]

    review = Habit(id=3, name="Weekly review",
                   description="Review the past week and plan the next one",
                   frequency=ExecutionFrequency.WEEKLY, start_date=start)
    review.executions = [execution(3, i + 1, week, "weekly review done")
                         for i, week in enumerate(weeks)]

    gym = Habit(id=4, name="Gym session", description="Go to the gym",
                frequency=ExecutionFrequency.WEEKLY, start_date=start)
    gym.executions = [execution(4, i + 1, week, "workout")
                      for i, week in enumerate(weeks) if i % 2 == 0]

    analysis = Habit(id=5, name="Learn Analysis 1",
                     description="Work through the Analysis 1 course material",
                     frequency=ExecutionFrequency.DAILY, start_date=start)
    analysis_days = [days[0], days[2], days[5], days[9], days[14], days[20], days[27]]
    analysis.executions = [execution(5, i + 1, day, "studied")
                           for i, day in enumerate(analysis_days)]

    return [water, reading, review, gym, analysis]


def main() -> None:
    """Generates the sample data and writes it to the given output file."""
    parser = argparse.ArgumentParser(description="Generate the predefined sample data")
    parser.add_argument("--output", default="data/repository.json",
                        help="output json file (default: data/repository.json)")
    args = parser.parse_args()
    habits = build_habits()
    HabitJsonSerializer().write_to_file(args.output, habits)
    print(f"Wrote {len(habits)} habits with "
          f"{sum(len(h.executions) for h in habits)} executions to {args.output}")


if __name__ == "__main__":
    main()
