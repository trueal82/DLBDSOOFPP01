"""
Rich Tui module as a simple user interface for Habito
"""

from collections.abc import Callable
from enum import Enum
from typing import Any

from rich.console import Console
from rich.panel import Panel
from rich.prompt import IntPrompt, Prompt
from rich.table import Table

from models.models import Habit, HabitExecution
from services.habit_service import HabitService
from utils.analytics import Streak

MenuItem = tuple[str, Callable[[], None]]


class RichTui:
    """
    RichTui is a text-based user interface (TUI) for the habit tracker application.
    """

    def __init__(self, habit_service: HabitService) -> None:
        self.habit_service: HabitService = habit_service
        self.console = Console()
        self.menu: dict[int, MenuItem] = {
            1: ("Show today's habits", self.print_due_habits),
            2: ("Add habit", self.add_habit),
            3: ("Mark habit done", self.execute_habit),
            4: ("Show history", self.show_history),
            5: ("Delete a habit", self.delete_habit),
            6: ("Analytics: habits by periodicity", self.show_habits_by_periodicity),
            7: ("Analytics: longest streak of all habits", self.show_longest_streak_all),
            8: ("Analytics: longest streak of one habit", self.show_longest_streak_for_habit),
            9: ("Show all habits", self.print_all_habits),
        }

    # Entry point
    #############
    def run(self) -> int:
        """Main entry point for the TUI application. Runs the menu loop until
        the user chooses to quit."""
        self.main_menu()
        return 0

    # Main menu
    ###########
    def show_main_menu(self) -> None:
        """Displays the main menu to the user."""
        table = Table.grid(padding=(0, 2))
        table.add_column(justify="right", style="cyan", no_wrap=True)
        table.add_column(style="white")
        for number, (label, _) in self.menu.items():
            table.add_row(str(number), label)
        table.add_row("0", "Quit")

        self.console.print(
            Panel(
                table,
                title="[bold]Habit Tracker[/bold]",
                border_style="blue",
            )
        )

    def ask_menu_choice(self) -> int:
        """Asks the user to choose a menu option (a menu entry or 0 to quit)."""
        choices = [str(number) for number in self.menu] + ["0"]
        return IntPrompt.ask(
            "Choose an option",
            choices=choices,
            default="1",
            show_choices=False,
        )

    def main_menu(self) -> None:
        """Main menu loop: displays the menu and dispatches the user's choice
        until the user quits."""
        while True:
            self.show_main_menu()
            choice: int = self.ask_menu_choice()
            if choice == 0:
                self.console.print("Exiting the application...")
                return
            self.main_route_to_selected_option(choice)

    def main_route_to_selected_option(self, choice: int) -> None:
        """Router method to map the user's choice to the menu's handler."""
        menu_item: MenuItem | None = self.menu.get(choice)
        if menu_item is None:
            self.console.print("[red]Invalid choice. Please try again.[/red]")
            return
        menu_item[1]()

    # Printer
    #########
    def pretty(self, ugly: Any) -> str:
        """Helper to make ugly pretty for console output"""
        if isinstance(ugly, Enum):
            return str(ugly.value)
        return str(ugly)

    def print_habits_as_table(self, habits: list[Habit],
                              visible_keys: list[str] | None = None) -> None:
        """Prints the given habits as a rich table."""
        table: Table = Table(padding=(0, 2),
                             title="[bold]Habits[/bold]", )

        if visible_keys is None:
            keys = list(Habit.model_fields)
        else:
            keys = visible_keys

        for key in keys:
            table.add_column(key, justify="center", style="cyan", no_wrap=True)

        for habit in habits:
            col = [getattr(habit, key, "") for key in keys]
            table.add_row(*[self.pretty(value) for value in col])

        self.console.print(table)

    def print_executions_as_table(self, executions: list[HabitExecution]) -> None:
        """Prints the given executions as a rich table."""
        table: Table = Table(padding=(0, 2), title="[bold]Executions[/bold]")
        for key in ["id", "date", "comment"]:
            table.add_column(key, justify="center", style="cyan")
        for item in executions:
            table.add_row(str(item.id), str(item.date), item.comment)
        self.console.print(table)

    def ask_habit_id(self, message: str) -> int | None:
        """Prints all habits and asks the user for a habit id. Returns None if
        the user enters 0."""
        self.print_all_habits()
        habit_id: int = IntPrompt.ask(f"{message} (id, 0 to cancel)", default=0)
        return habit_id or None

    # Show all habits
    #################
    def print_all_habits(self) -> None:
        """Prints all habits"""
        habits = self.habit_service.get_all_habits()
        visible_keys: list[str] = ["id", "name", "description", "frequency"]
        self.print_habits_as_table(habits, visible_keys=visible_keys)

    # Print due habits
    ##################
    def print_due_habits(self) -> None:
        """Prints all habits that are due today."""
        habits = self.habit_service.get_due_habits()
        if not habits:
            self.console.print("Nothing due today. Well done!")
            return
        visible_keys: list[str] = ["id", "name", "description", "frequency"]
        self.print_habits_as_table(habits, visible_keys=visible_keys)

    # Adding habit
    ##############
    def add_habit(self) -> None:
        """Walks the user through the fields of a new habit and stores it."""
        while True:
            name: str = Prompt.ask("Habit name?")
            if name.strip():
                break
            self.console.print("[red]Habit name cannot be empty.[/red]")
        description: str = Prompt.ask("Habit description?", default="")
        frequency: str = Prompt.ask("Habit frequency?",
                                    choices=self.habit_service.get_execution_frequencies(),
                                    default="daily")
        self.habit_service.add_habit(name=name, description=description,
                                     frequency=frequency)
        self.console.print(f"[green]Habit '{name}' added.[/green]")

    # Execute habit
    ###############
    def execute_habit(self) -> None:
        """Marks a habit chosen by the user as done today."""
        self.print_due_habits()
        habit_id: int | None = self.ask_habit_id("Which habit do you want to execute?")
        if habit_id is None:
            return
        comment: str = Prompt.ask("Optional comment?", default="")
        try:
            self.habit_service.execute_habits(habit_id=habit_id, comment=comment)
        except ValueError as error:
            self.console.print(f"[red]{error}[/red]")
            return
        self.console.print("[green]Habit marked as done.[/green]")

    # Show history
    ##############
    def show_history(self) -> None:
        """Prints all executions of a habit chosen by the user."""
        habit_id: int | None = self.ask_habit_id("Which habit's history do you want to see?")
        if habit_id is None:
            return
        try:
            habit: Habit = self.habit_service.get_habit_by_id(habit_id)
        except ValueError as error:
            self.console.print(f"[red]{error}[/red]")
            return
        self.console.print(f"History for [bold]{habit.name}[/bold]")
        self.print_executions_as_table(habit.executions)

    # Delete habit
    ##############
    def delete_habit(self) -> None:
        """Deletes a habit chosen by the user, after confirmation."""
        habit_id: int | None = self.ask_habit_id("Which habit do you want to delete?")
        if habit_id is None:
            return
        habit: Habit = self.habit_service.get_habit_by_id(habit_id)
        confirmed: str = Prompt.ask(
            f"Really delete '{habit.name}' and all its executions?",
            choices=["y", "n"], default="n")
        if confirmed != "y":
            return
        self.habit_service.delete_habit(habit_id)
        self.console.print(f"[green]Habit '{habit.name}' deleted.[/green]")

    # Analytics
    ###########
    def show_habits_by_periodicity(self) -> None:
        """Prints all habits with a periodicity chosen by the user."""
        frequency: str = Prompt.ask("Which periodicity?",
                                    choices=self.habit_service.get_execution_frequencies(),
                                    default="daily")
        habits = self.habit_service.get_habits_by_periodicity(frequency)
        self.console.print(f"All [bold]{frequency}[/bold] habits:")
        self.print_habits_as_table(
            habits, visible_keys=["id", "name", "description", "frequency"])

    def show_longest_streak_all(self) -> None:
        """Prints the longest streak of all habits."""
        self.print_streak(self.habit_service.get_longest_streak_all())

    def show_longest_streak_for_habit(self) -> None:
        """Prints the longest streak of a habit chosen by the user."""
        habit_id: int | None = self.ask_habit_id(
            "Which habit's longest streak do you want to see?")
        if habit_id is None:
            return
        try:
            self.print_streak(self.habit_service.get_longest_streak_for_habit(habit_id))
        except ValueError as error:
            self.console.print(f"[red]{error}[/red]")

    def print_streak(self, streak: Streak | None) -> None:
        """Prints a streak, or a hint if there is none."""
        if streak is None:
            self.console.print("No streak found - the habit was never executed.")
            return
        self.console.print(
            f"Longest streak of [bold]{streak.habit_name}[/bold]: "
            f"[green]{streak.length}[/green] consecutive "
            f"{streak.frequency.value} period(s) "
            f"({streak.start} to {streak.end})")
