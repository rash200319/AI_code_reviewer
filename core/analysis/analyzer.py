# ai-code-reviewer/core/analysis/analyzer.py
import ast
from typing import List, Dict, Any

class MagicNumberVisitor(ast.NodeVisitor):
    """
    AST visitor to find instances of 'Magic Numbers' (raw, hardcoded numbers) 
    in assignment statements and simple expressions.
    """
    def __init__(self):
        self.issues = []

    def visit_Constant(self, node):
        """Called for literal constant values like 5, 100, "hello"."""
        # Check if the constant is an integer or float (but not 0, 1, -1)
        if isinstance(node.value, (int, float)):
            # Ignore common constants like 0, 1, -1, 2 (often used for loops, booleans, etc.)
            if abs(node.value) > 2 and not isinstance(node.value, bool):
                self.issues.append({
                    "type": "MagicNumber",
                    "line": node.lineno,
                    "col": node.col_offset,
                    "value": node.value,
                    "message": f"Found magic number: {node.value}. Consider using a named constant."
                })
        
        # Continue traversing the children of this node
        self.generic_visit(node)


class Analyzer:
    """
    Performs static code analysis on a given Python file content.
    """
    def __init__(self, code: str):
        self.code = code

    def analyze(self) -> List[Dict[str, Any]]:
        """Parses the code and runs all checks."""
        issues = []
        try:
            # 1. Parse the code into an Abstract Syntax Tree (AST)
            tree = ast.parse(self.code)
            
            # 2. Run the MagicNumber check
            visitor = MagicNumberVisitor()
            visitor.visit(tree)
            issues.extend(visitor.issues)

        except SyntaxError as e:
            print(f"Error: Could not parse file due to a Syntax Error on line {e.lineno}.")
        except Exception as e:
            print(f"An unexpected analysis error occurred: {e}")
            
        return issues