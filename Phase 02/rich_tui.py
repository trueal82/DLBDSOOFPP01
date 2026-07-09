import config

from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.table import Table
from rich.panel import Panel

from datetime import date

class RichTui:
    def __init__(self, habit_service: HabitService) -> None:
        self.habit_service = habit_service
        self.console = Console()

    def show_menu(self) -> None:
        table = Table.grid(padding=(0, 2))
        table.add_column(justify="right", style="cyan", no_wrap=True)
        table.add_column(style="white")
        table.add_row("1", "Show today's habits")
        table.add_row("2", "Add habit")
        table.add_row("3", "Mark habit done")
        table.add_row("4", "Show history")
        table.add_row("5", "Quit")

        self.console.print(
            Panel(
                table,
                title="[bold]Habit Tracker[/bold]",
                border_style="blue",
            )
        )

    def ask_menu_choice(self) -> str:
        return Prompt.ask(
            "Choose an option",
            choices=["1", "2", "3", "4", "5"],
            default="1",
            show_choices=False,
        )

    def show_menu(self) -> None:
        table = Table.grid(padding=(0, 2))
        table.add_column(justify="right", style="cyan", no_wrap=True)
        table.add_column(style="white")
        table.add_row("1", "Show today's habits")
        table.add_row("2", "Add habit")
        table.add_row("3", "Mark habit done")
        table.add_row("4", "Show history")
        table.add_row("5", "Quit")

        self.console.print(
            Panel(
                table,
                title="[bold]Habit Tracker[/bold]",
                border_style="blue",
            )
        )

    def ask_menu_choice(self) -> str:
        return Prompt.ask(
            "Choose an option",
            choices=["1", "2", "3", "4", "5"],
            default="1",
            show_choices=False,
        )

    def main_menu(self) -> None:
        # Run the main loop here
        user_wants_to_exit = False
        while not user_wants_to_exit:
            # Your main code logic here
            self.show_menu()
            self.main_route_to_selected_option(self.ask_menu_choice())

    def main_route_to_selected_option(self, choice: str) -> None:
        if choice == "1":
            # Show today's habits
            pass
        elif choice == "2":
            # Add habit
            pass
        elif choice == "3":
            # Mark habit done
            pass
        elif choice == "4":
            # Show history
            pass
        elif choice == "5":
            # Quit the application
            print("Exiting the application...")
            exit(0)
        else:
            print("Invalid choice. Please try again.")

    def run(self):
        """Main entry point for the TUI application."""
        self.main_menu()