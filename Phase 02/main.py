import config
import logging
import argparse

from rich_tui import RichTui
from habit_service import HabitService
from imp_ex import ImpEx

def setup_logging() -> None:
    logging.basicConfig(
        level=config.LOG_LEVEL,
        format="%(asctime)s %(levelname)-8s [%(name)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

def setup_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-r", "--read-from-file", type=str,
                        help="Read habits from a file", required=False, )
    parser.add_argument("-w", "--write-to-file", type=str,
                        help="Write habits to a file", required=False)
    return parser.parse_args()


def main():
    setup_logging()
    args = setup_args()
    service = HabitService()

    if not any(vars(args).values()):
        app = RichTui(service)
        app.run()
        return 0
    else:
        app = ImpEx(service)
        app.run(args)
        return 0


if __name__ == "__main__":
    # Your main code logic here
    raise SystemExit(main())