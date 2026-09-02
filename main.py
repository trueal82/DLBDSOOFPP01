"""
The main file to glue things together
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


def setup_args():
    """Setup arguments parsing"""
    parser = argparse.ArgumentParser()
    parser.add_argument("-r", "--read-from-file", type=str,
                        help="Read habits from a file", required=False, )
    parser.add_argument("-w", "--write-to-file", type=str,
                        help="Write habits to a file", required=False)
    return parser.parse_args()


def main():
    """The main function"""
    setup_logging()
    args = setup_args()
    service = HabitService()

    if not any(vars(args).values()):
        app = RichTui(service)
        return app.run()

    app = CLI(service)
    return app.run(args)


if __name__ == "__main__":
    # Your main code logic here
    raise SystemExit(main())
