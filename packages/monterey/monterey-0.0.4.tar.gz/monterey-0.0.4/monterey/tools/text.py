from rich.console import Console
from rich.panel import Panel
from rich import box
from rich.columns import Columns
from rich.syntax import Syntax
from art import text2art
import random

#==============================================================================

class Text:
    """
    Dynamic, interchangeable text styling for the terminal using the Rich library.
    
    Attributes:
        console: A Rich Console instance for styled output.
    """
    def __init__(self):
        self.console = Console()

    def display(self, message: str = None, style: str = "bold white", use_box: bool = False):
            """
            Displays a message on the console.

            Args:
                message (str, optional): The message to be displayed. Defaults to None.
                style (str, optional): The style of the message. Defaults to "bold white".
                use_box (bool, optional): Whether to display the message in a box. Defaults to False.
            """
            if not message:
                message = """
                No message provided.
                """

            if isinstance(message, list):
                if use_box:
                    columns = Columns([Panel(item, expand=False, box=box.ROUNDED) for item in message])
                else:
                    columns = Columns([Panel(item, expand=False) for item in message])
                self.console.print(columns, style=style)
            else:
                if use_box:
                    message = Panel(message, expand=False, box=box.ROUNDED)
                self.console.print(message, style=style)

    def code(self, code: str = None, language: str = "python", theme: str = "monokai", line_numbers: bool = True):
        """
        Style and print a block of code using Rich Syntax.

        Example:
        ```python
        from yosemite.tools.text import Text
        text = Text()
        code = '''
        def main():
            text = Text()
            text.say("Hello, Rich!")
        '''
        text.code(code, language="python", theme="monokai", line_numbers=True)
        ```

        Args:
            code (str): The code to be styled and printed.
            language (str, optional): The language of the code. Defaults to "python".
            theme (str, optional): The theme of the code. Defaults to "monokai".
            line_numbers (bool, optional): Whether to display line numbers. Defaults to True.
        """
        if not code:
            code = """
            No code provided.
            """

        syntax = Syntax(code, language, theme=theme, line_numbers=line_numbers)
        self.console.print(syntax)

    def splash(self, message="hammadpy", art="random"):
        """
        Creates an ASCII art styled splash 'logo' in the terminal using Rich Panel.

        Example:
            ```python
            from yosemite.tools.text import Text
            
            text = Text()
            text.splash("hammadpy", art="random")
            ```

        Args:
            message (str): The message to display in the splash. Defaults to "hammadpy".
            art (str): The ASCII art style to use. Defaults to "random".
        """
        if art == "random":
            fonts = ["block", "caligraphy", "doh", "dohc", "doom", "epic", "fender", "graffiti", "isometric1", "isometric2", "isometric3", "isometric4", "letters", "alligator", "dotmatrix", "bubble", "bulbhead", "digital", "ivrit", "lean", "mini", "script", "shadow", "slant", "speed", "starwars", "stop", "thin", "3-d", "3x5", "5lineoblique", "acrobatic", "alligator2", "alligator3", "alphabet", "banner", "banner3-D", "banner3", "banner4", "barbwire", "basic", "bell", "big", "bigchief", "binary", "block", "broadway", "bubble", "caligraphy", "doh", "dohc", "doom", "dotmatrix", "drpepper", "epic", "fender", "graffiti", "isometric1", "isometric2", "isometric3", "isometric4", "letters", "alligator", "dotmatrix", "bubble", "bulbhead", "digital", "ivrit", "lean", "mini", "script", "shadow", "slant", "speed", "starwars", "stop", "thin"]
            art = random.choice(fonts)

        art_message = text2art(message, font=art)
        panel = Panel(art_message, expand=False, border_style="bold dark_orange")
        self.console.print(panel)

    def header(self, message, style="bold white", underline="=", overline="="):
        """
        Style and print a header using Rich.

        Args:
            message (str): The message to be styled and printed.
            style (str, optional): The style of the text. Defaults to "bold white".
            underline (str, optional): The character to use for underlining. Defaults to "=".
            overline (str, optional): The character to use for overlining. Defaults to "=".
        """
        self.console.print(message, style=style)
        self.console.print(underline * len(message), style=style)

#==============================================================================

if __name__ == "__main__":
    text = Text()
    text.splash("hammadpy", art="random")
    text.display("Hello, Rich!", style="bold red", use_box=True)
    text.code("print('Hello, Rich!')", language="python", theme="monokai", line_numbers=True)
    text.header("Hello, Rich!", style="bold red", underline="-", overline="-")