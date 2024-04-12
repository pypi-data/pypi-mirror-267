from IPython.display import display, HTML
import os

class Tailwind:
    """
    A class for creating and displaying HTML elements with Tailwind CSS, Material-UI styles, and custom fonts in Jupyter notebooks.
    
    Attributes:
        html_template (str): The HTML template used to create the elements.
    """
    def __init__(self):
        self.html_template = """
        <!DOCTYPE html>
        <html>
        <head>
            <script src="https://cdn.tailwindcss.com"></script>
            <script src="https://unpkg.com/@material-ui/core@latest/umd/material-ui.development.js" crossorigin="anonymous"></script>
            <script src="https://unpkg.com/babel-standalone@latest/babel.min.js" crossorigin="anonymous"></script>
            <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Roboto:300,400,500,700&display=swap" />
            <link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;700&family=Lexend:wght@400;500;600;700&family=Lora:wght@400;500;600;700&family=Playfair+Display:wght@400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
            <style>
                body {{
                    font-family: 'DM Sans', sans-serif;
                }}
                h1, h2, h3, h4, h5, h6 {{
                    font-family: 'Lexend', sans-serif;
                }}
                p {{
                    font-family: 'Lora', serif;
                }}
                code, pre {{
                    font-family: 'JetBrains Mono', monospace;
                }}
                .playfair {{
                    font-family: 'Playfair Display', serif;
                }}
            </style>
        </head>
        <body>
            <div id="root"></div>
            <script type="text/babel">
                const {{ content }} = MaterialUI;
                ReactDOM.render(
                    <div>
                        {content}
                    </div>,
                    document.getElementById('root')
                );
            </script>
        </body>
        </html>
        """

    def display(self, content: str, className: str = "", component: str = "div", mui: bool = False):
        """
        Display the HTML element with the specified content, component type, Tailwind CSS class, and optionally use Material-UI.

        Args:
            content (str): The content of the HTML element.
            component (str, optional): The HTML component type. Defaults to "div".
            className (str, optional): The Tailwind CSS class name. Defaults to an empty string.
            mui (bool, optional): Whether to use Material-UI components. Defaults to False.
        """
        if mui:
            element = f"<{component} className='{{{{ classes.root }}}} {className}'>{content}</{component}>"
            mui_imports = "{ Button, Typography }"
            html = self.html_template.format(content=element, mui_imports=mui_imports)
        else:
            element = f"<{component} class='{className}'>{content}</{component}>"
            html = self.html_template.format(content=element, mui_imports="")
        
        display(HTML(html))

# Example usage
if __name__ == "__main__":
    tailwind = Tailwind()
    tailwind.display("Hello, Tailwind!", component="h1", className="text-4xl font-bold text-blue-500")
    tailwind.display("Hello, Material-UI!", component="Button", className="bg-blue-500 text-white px-4 py-2 rounded", mui=True)
    tailwind.display("This is a paragraph with Lora font.", component="p", className="text-lg")
    tailwind.display("This is a code snippet with JetBrains Mono font.", component="code", className="text-sm")
    tailwind.display("This is a heading with Playfair Display font.", component="h2", className="text-3xl playfair")