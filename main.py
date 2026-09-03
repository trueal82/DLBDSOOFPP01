"""
The main file to glue things together.

Thin wrapper so the app can also be started with ``python main.py`` from
the repository root. The installed package provides the ``habito`` command
(see pyproject.toml).
"""
from habito import main

if __name__ == "__main__":
    raise SystemExit(main())
