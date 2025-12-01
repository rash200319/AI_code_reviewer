# ai-code-reviewer/core/detectors/magic_number_detector.py
import ast
from typing import List, Dict, Any

class MagicNumberDetector(ast.NodeVisitor):
    """
    Detects "magic numbers" (unnamed numeric literals) in the code.
    This class inherits from ast.NodeVisitor to efficiently traverse the AST.
    """
    
    def __init__(self):
        # List to store the issues found
        self.issues: List[Dict[str, Any]] = []

    def visit_Constant(self, node):
        """Called when an ast.Constant node is encountered (where numbers are stored)."""
        
        # We only care about numeric constants (integers or floats)
        if isinstance(node.value, (int, float)):
            
            # 1. Ignore common numbers (0, 1, -1) often used for loop boundaries or checks
            if abs(node.value) <= 1:
                return

            # --- Simplified Logic for MVP ---
            # We treat any number > 1 or < -1 as a potential magic number.
            
            self.issues.append({
                "type": "MagicNumber",
                # ast nodes carry line and column info!
                "line": node.lineno,
                "col": node.col_offset,
                "value": node.value,
                "message": f"Found magic number: {node.value}. Consider using a named constant."
            })
        
        # Ensure we continue traversing the rest of the AST
        # This is required to process child nodes of the current node
        self.generic_visit(node)
        
    def get_issues(self) -> List[Dict[str, Any]]:
        return self.issues