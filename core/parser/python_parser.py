# ai-code-reviewer/core/parser/python_parser.py
import ast
from typing import List

class PythonParser:
    """
    Parses Python code into an AST and extracts basic information.
    """

    @staticmethod
    def load_code(filepath: str) -> str:
        """Loads and returns the source code from a file."""
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()

    @staticmethod
    def parse_ast(code: str) -> ast.AST:
        """Parses the source code string into a Python AST."""
        # The 'type_comments=True' is useful for advanced static analysis
        return ast.parse(code, type_comments=True)

    @staticmethod
    def find_function_names(tree: ast.AST) -> List[str]:
        """Traverses the AST to find all defined function names."""
        function_names = []
        # Use ast.walk to iterate over all nodes in the tree
        for node in ast.walk(tree):
            # Check if the node is a FunctionDef (standard function)
            if isinstance(node, ast.FunctionDef):
                function_names.append(node.name)
            # Check if the node is an AsyncFunctionDef (async function)
            elif isinstance(node, ast.AsyncFunctionDef):
                function_names.append(node.name)
        return function_names