from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.shortcuts import yes_no_dialog

class Input:
    def __init__(self):
        """
        A lighweight for handling user inputs in the terminal.
        Uses Prompt Toolkit for both simple CLI text and expressive GUI dialogs.

        Attributes:
            pause: A method to pause the terminal until the user presses Enter.
            confirm: A method to prompt the user for a yes/no confirmation.
            ask: A method to prompt the user for input in the terminal.
            choice: A method to prompt the user to select from a list of choices.
        """
        pass

    @staticmethod
    def pause(message: str = None):
        """
        Pauses the terminal until the user presses Enter.
        
        Example:
            ```python
            from yosemite.tools.input import Input

            Input.pause()
            ```

        Args:
            message (str): The message to display to the user.
            """
        if not message:
            message = """
Press Enter to continue...

"""

    @staticmethod
    def confirm(message: str = None):
        """
        Prompt the user for a yes/no confirmation.

        Example:
            ```python
            Input.confirm("Are you sure?")
            ```

        Args:
            message (str): The message to display to the user.
        """
        if not message:
            message = ""
        if message:
            value = yes_no_dialog(title="Confirmation", text=message).run()
            return value
        else:
            print("'message' is required for prompt_confirmation()")

    @staticmethod
    def ask(message: str = None):
        """
        Prompt the user for input in the terminal.

        Example:
            ```python
            name = Input.ask("What is your name?")
            print(f"Hello, {name}!")
            ```

            ```bash
            Hello, John!
            ```

        Args:
            message (str): The message to display to the user.
        """
        if not message:
            message = """
"""     
        if message:
            message = f"""
{message}

"""
        if message:
            value = prompt(message)
            return value
        else:
            print("'message' is required for prompt_input()")

    @staticmethod
    def choice(message: str = None, choices: list = None):
        """
        Prompt the user to select from a list of choices.

        Example:
            ```python
            list = ["Red", "Green", "Blue"]
            color = Input.choice("Choose a color:", list)
            print(f"You chose {color}.")
            ```

            ```bash
            You chose Red.
            ```

        Args:
            message (str): The message to display to the user.
            choices (list): A list of choices for the user to select from.
        """
        if not message:
            message = """
"""
        if message:
            message = f"""
{message}

"""
        if message and choices:
            value = prompt(message=message, completer=WordCompleter(words=choices))
            return value
        else:
            print("'message' and 'choices' are required for prompt_choice()")

#==============================================================================#

if __name__ == "__main__":
    list = ["Red", "Green", "Blue"]
    Input.pause()
    Input.ask("What is your name?")
    Input.confirm("Are you sure?")
    Input.choice("Choose a color:", list)