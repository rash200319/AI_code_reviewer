# ai-code-reviewer/cli/main.py
import click  #command line interface library
import os
from core.parser.python_parser import PythonParser

@click.command()
@click.argument('path', type=click.Path(exists=True))
def analyze(path: str):
    """
    The main CLI entrypoint for the AI Code Reviewer.
    Analyzes a Python file or directory for code smells.
    """
    if os.path.isdir(path):
        # We'll expand this later to recursively find all .py files
        click.echo(f"Directory analysis is not yet implemented. Please specify a file.")
        return

    # --- File Loader & AST Parser (The Week 1 Goal) ---
    try:
        click.echo(f"Starting analysis for: {path}")
        
        # 1. Load the file content
        code = PythonParser.load_code(path)
        click.echo("File loaded.")

        # 2. Parse the code into an AST
        tree = PythonParser.parse_ast(code)
        click.echo("AST generated.")
        
        # 3. Simple proof-of-concept analysis (Finding function names)
        function_names = PythonParser.find_function_names(tree)
        
        click.echo("\n Basic Structure Analysis:")
        click.echo(f"  Found {len(function_names)} function(s): {', '.join(function_names)}")

    except Exception as e:
        click.echo(f" An error occurred during parsing: {e}")

if __name__ == '__main__':
    # To run: python -m cli.main <path/to/file.py>
    analyze()