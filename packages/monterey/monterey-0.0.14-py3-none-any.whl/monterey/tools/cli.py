import fire

#==============================================================================

class CLI:
    def __init__(self):
        """
        A lightweight framework for creating CLI apps using Python Fire.

        This class provides a simple and intuitive way to define and run CLI
        commands using Python Fire. It allows you to quickly create powerful
        CLI apps with minimal boilerplate code.

        Attributes:
            command: A decorator to define a CLI command.
            run: A function to run the CLI app.

        Example:
            ```python
            from yosemite.tools.cli import CLI

            @CLI.command()
            def hello(name="World"):
                return f"Hello, {name}!"

            @CLI.command(name="greet")
            def greeting(name="World"):
                return f"Greetings, {name}!"

            if __name__ == "__main__":
                CLI.run()
            ```

            This example defines two CLI commands: `hello` and `greet`. The `hello`
            command takes an optional `name` argument and returns a hello message.
            The `greet` command also takes an optional `name` argument and returns
            a greeting message.

            To run the CLI app, simply call `CLI.run()` at the end of the script.

            ```
            $ python example.py hello
            Hello, World!

            $ python example.py hello --name="Alice"
            Hello, Alice!

            $ python example.py greet
            Greetings, World!

            $ python example.py greet --name="Bob"
            Greetings, Bob!
            ```
        """
        pass

    @staticmethod
    def create(name=None, **kwargs):
        """
        A decorator to define a CLI command.

        This decorator is used to define a function as a CLI command. It wraps
        the function with the `fire.decorators.SetMetadata` decorator from
        Python Fire, which sets the command name and any additional metadata.

        Args:
            name (str): The name of the command. If not provided, the function
                        name is used as the command name.
            **kwargs: Additional keyword arguments to pass to the Fire decorator.

        Returns:
            The decorated function.

        Example:
            ```python
            @CLI.command()
            def hello(name="World"):
                return f"Hello, {name}!"

            @CLI.command(name="greet")
            def greeting(name="World"):
                return f"Greetings, {name}!"
            ```

            In this example, the `hello` function is defined as a CLI command
            with the same name as the function. The `greeting` function is also
            defined as a CLI command, but with the name "greet".
        """
        def decorator(func):
            return fire.decorators.SetMetadata(func, name, **kwargs)
        return decorator

    @staticmethod
    def run(component=None, **kwargs):
        """
        A function to run the CLI app.

        This function runs the CLI app using Python Fire. It takes an optional
        `component` argument, which specifies the component to run the CLI app
        on. If not provided, the calling module is used.

        Args:
            component: The component to run the CLI app on. If not provided,
                       the calling module is used.
            **kwargs: Additional keyword arguments to pass to the Fire CLI.

        Example:
            ```python
            if __name__ == "__main__":
                CLI.run()
            ```

            This example runs the CLI app on the calling module.

            ```python
            def main():
                CLI.run(component=some_module)

            if __name__ == "__main__":
                main()
            ```

            This example runs the CLI app on the specified `some_module` component.
        """
        if component is None:
            fire.Fire(**kwargs)
        else:
            fire.Fire(component, **kwargs)

#==============================================================================

"""
To test this script, try running the following commands:

$ python cli.py hello
Hello, World!

$ python cli.py hello --name="Alice"
Hello, Alice!
"""

if __name__ == "__main__":
    @CLI.create()
    def hello(name="World"):
        """
        A simple command that greets the user.

        Args:
            name (str): The name to greet. Defaults to "World".

        Returns:
            A greeting message.
        """
        return f"Hello, {name}!"

    @CLI.create(name="greet")
    def greeting(name="World"):
        """
        A command that generates a greeting message.

        Args:
            name (str): The name to include in the greeting. Defaults to "World".

        Returns:
            A greeting message.
        """
        return f"Greetings, {name}!"

    CLI.run()