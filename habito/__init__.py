"""
The main package of Habito: glues configuration, clients and services together.
"""
import argparse
import logging

import config
from clients.cli import CLI
from clients.rich_tui import RichTui
from services.habit_service import HabitService


def setup_logging() -> None:
    """Setup logging"""
    logging.basicConfig(
        level=config.LOG_LEVEL,
        format="%(asctime)s %(levelname)-8s [%(name)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def setup_args() -> argparse.Namespace:
    """Setup arguments parsing"""
    parser = argparse.ArgumentParser(
        prog="habito",
        description="A simple habit tracker. Start without arguments to get "
                    "an interactive menu.")
    parser.add_argument("-r", "--read-from-file", type=str, metavar="FILE",
                        help="Import habits (and their executions) from a json file",
                        required=False)
    parser.add_argument("-w", "--write-to-file", type=str, metavar="FILE",
                        help="Export all habits (and their executions) to a json file",
                        required=False)
    parser.add_argument("-d", "--delete-habit", type=int, metavar="ID",
                        help="Delete the habit with the given id",
                        required=False)
    parser.add_argument("-a", "--analyse", action="store_true",
                        help="Print the analytics summary and exit",
                        required=False)
    return parser.parse_args()


def main() -> int:
    """The main function. Without command line arguments it starts the
    interactive TUI, otherwise the non-interactive CLI client."""
    setup_logging()
    args = setup_args()
    service = HabitService()

    if not any(vars(args).values()):
        app = RichTui(service)
        return app.run()

    app = CLI(service)
    return app.run(args)


if __name__ == "__main__":
    raise SystemExit(main())
