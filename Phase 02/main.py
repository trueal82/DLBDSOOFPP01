import config
import logging

from rich_tui import RichTui
from habit_service import HabitService

def setup_logging() -> None:
    logging.basicConfig(
        level=config.LOG_LEVEL,
        format="%(asctime)s %(levelname)-8s [%(name)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

def main():
    setup_logging()
    service = HabitService()
    # consider making this async to be able to spawn an API server at the same time
    app = RichTui(service) 
    app.run()
    return 0

if __name__ == "__main__":
    # Your main code logic here
    raise SystemExit(main())