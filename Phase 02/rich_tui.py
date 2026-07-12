import string

from rich.console import Console
from rich.panel import Panel
from rich.prompt import IntPrompt, Prompt, PromptBase
from rich.table import Table

from habit_service import HabitService


class RichTui:
    """
    RichTui is a text-based user interface (TUI) for the habit tracker application.
    """

    def __init__(self, habit_service: HabitService) -> None:
        self.habit_service: HabitService = habit_service
        self.console = Console()

    def show_main_menu(self) -> None:
        """Displays the main menu to the user."""
        table = Table.grid(padding=(0, 2))
        table.add_column(justify="right", style="cyan", no_wrap=True)
        table.add_column(style="white")
        table.add_row("1", "Show today's habits")
        table.add_row("2", "Add habit")
        table.add_row("3", "Mark habit done")
        table.add_row("4", "Show history")
        table.add_row("5", "Show all habits")
        table.add_row("9", "Quit")

        self.console.print(
            Panel(
                table,
                title="[bold]Habit Tracker[/bold]",
                border_style="blue",
            )
        )

    def ask_menu_choice(self) -> int:
        return int(IntPrompt.ask(
            "Choose an option",
            choices=["1", "2", "3", "4", "5", "9"],
            default="1",
            show_choices=False,
        ))

    def main_menu(self) -> None:
        # Run the main loop here
        while True:
            # Your main code logic here
            self.show_main_menu()
            self.main_route_to_selected_option(self.ask_menu_choice())

    def main_route_to_selected_option(self, choice: int) -> None:
        if choice == 1:
            # Show today's habits
            pass
        elif choice == 2:
            self.add_habit()
            pass
        elif choice == 3:
            # Mark habit done
            pass
        elif choice == 4:
            # Show history
            pass
        elif choice == 5:
            # Show all habits
            self.print_all_habits()
        elif choice == 9:
            # Quit the application
            print("Exiting the application...")
            exit(0)
        else:
            print("Invalid choice. Please try again.")

    def print_all_habits(self) -> None:
        habits = self.habit_service.get_all_habits()
        with self.console.pager():
            for habit in habits:
                self.console.print_json(habit.model_dump_json(indent=2))

    def run(self):
        """Main entry point for the TUI application."""
        self.main_menu()

    def add_habit(self):
        name: str = Prompt.ask("Habbit name?")
        if not name: return
        description: str = Prompt.ask("Habit description?")
        frequency = PromptBase.ask("Habit frequency?",
                                    choices=self.habit_service.get_execution_frequencies())
        self.habit_service.add_habit(name=name, description=description, frequency=frequency)

