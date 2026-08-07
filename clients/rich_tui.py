"""
Rich Tui module as a simple user interface for Habito
"""

import sys
from enum import Enum

from rich.console import Console
from rich.panel import Panel
from rich.prompt import IntPrompt, Prompt, PromptBase
from rich.table import Table

from models.models import Habit
from services.habit_service import HabitService


class RichTui:
    """
    RichTui is a text-based user interface (TUI) for the habit tracker application.
    """

    def __init__(self, habit_service: HabitService) -> None:
        self.habit_service: HabitService = habit_service
        self.console = Console()

    # Entry point
    #############
    def run(self):
        """Main entry point for the TUI application."""
        self.main_menu()
        return 0

    # Main menu
    ###########
    def show_main_menu(self) -> None:
        """Displays the main menu to the user."""
        table = Table.grid(padding=(0, 2))
        table.add_column(justify="right", style="cyan", no_wrap=True)
        table.add_column(style="white")
        table.add_row("1", "Show today's habits")
        table.add_row("2", "Add habit")
        table.add_row("3", "Mark habit done")
        table.add_row("4", "Show history")
        table.add_row("8", "Show all habits")
        table.add_row("9", "Quit")

        self.console.print(
            Panel(
                table,
                title="[bold]Habit Tracker[/bold]",
                border_style="blue",
            )
        )

    def ask_menu_choice(self, upper: int | None = None) -> int:
        """
        Asks user to choose an option
        :return:
        """
        if not upper:
            upper = 10
        return int(IntPrompt.ask(
            "Choose an option",
            choices=[str(value) for value in range(1, upper)],  # event *Int*Prompt needs list[str]
            default="1",
            show_choices=False,
        ))

    def main_menu(self) -> None:
        """
        Main menu method to display the main menu
        :return:
        """
        # Run the main loop here
        while True:
            # Your main code logic here
            self.show_main_menu()
            self.main_route_to_selected_option(self.ask_menu_choice(upper=10))

    def main_route_to_selected_option(self, choice: int) -> None:
        """
        Router method to map input to method calls
        :param choice:
        :return:
        """
        if choice == 1:
            self.print_due_habits()
            # Show today's habits
        elif choice == 2:
            self.add_habit()
        elif choice == 3:
            self.execute_habit()
            # Mark habit done
        elif choice == 4:
            pass
            # Show history
        elif choice == 8:
            # Show all habits
            self.print_all_habits()
        elif choice == 9:
            # Quit the application
            print("Exiting the application...")
            sys.exit(0)
        else:
            print("Invalid choice. Please try again.")

    # Printer
    #########
    def pretty(self, ugly: Any) -> str:
        """Helper to make ugly pretty for console output"""
        if isinstance(ugly, Enum):
            return str(ugly.value)
        return str(ugly)

    def print_habits_as_table(self, habits: list[Habit], visible_keys: list[str] | None = None) -> None:
        table: Table = Table(padding=(0, 2),
                             title="[bold]Habits[/bold]", )

        if visible_keys is None:
            keys = Habit.model_fields
        else:
            keys = visible_keys

        for key in keys:
            table.add_column(key, justify="center", style="cyan", no_wrap=True)

        for habit in habits:
            col = []
            for key in keys:
                col.append(getattr(habit, key, ""))
            table.add_row(*[self.pretty(value) for value in col])

        self.console.print(table)

    # Show all habits
    #################

    def print_all_habits(self) -> None:
        """
        Prints all habits
        :return:
        """
        habits = self.habit_service.get_all_habits()
        visible_keys: list[str] = ["name", "description", "frequency"]
        self.print_habits_as_table(habits, visible_keys=visible_keys)

    # Adding habbit
    def add_habit(self):
        """
        Add habit to the habit_service
        :return:
        """
        name: str = Prompt.ask("Habit name?")
        if not name:
            raise ValueError("Habit name cannot be empty.")
        description: str = Prompt.ask("Habit description?")
        frequency = PromptBase.ask("Habit frequency?",
                                   choices=self.habit_service.get_execution_frequencies())
        self.habit_service.add_habit(name=name, description=description, frequency=frequency)

    # Print due habits
    ##################
    def print_due_habits(self) -> None:
        self.print_habits_as_table(self.habit_service.get_due_habits())

    # Exexute habit
    ###############
    def execute_habit(self) -> None:
        self.print_due_habits()
        h_id: int = int(IntPrompt.ask("Which habit do you want to execute? (id)"))
        h_comment: str = PromptBase.ask("Optional comment?")
        self.habit_service.execute_habits(habit_id=h_id, comment=h_comment)
        self.main_menu()
