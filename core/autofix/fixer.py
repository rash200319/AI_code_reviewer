# ai-code-reviewer/core/autofix/fixer.py (Updated with apply_fixes_from_report)
import os
import json
from typing import Dict, Any, List, Tuple

class Fixer:
    """
    Manages the creation and application of automatic code fixes (patches).
    """
    def __init__(self, code: str):
        self.code_lines = code.splitlines()

    def generate_fix(self, issue: Dict[str, Any]) -> Tuple[bool, str]:
        """Generates a fix description for a supported issue type."""
        issue_type = issue['type']
        line_num = issue['line']
        value = issue.get('value')
        
        if issue_type == "MagicNumber" and value is not None:
            # We will use a generic constant name for simplicity
            constant_name = f"MAGIC_NUM_{line_num}" 
            
            # This is the patch data stored in the report
            # The description explains the fix to the user in the dashboard
            description = (
                f"Define a new constant: `{constant_name} = {value}` (at the top of the file).\n"
                f"Replace the detected value `{value}` on line {line_num} with `{constant_name}`."
            )
            
            # The patch data itself (used by the apply_fixes_from_report method)
            # Storing the specific line change instruction is easier than using a full diff format
            issue['fix_patch'] = {
                "constant_name": constant_name,
                "constant_value": value,
                "line_to_replace": line_num,
                "old_code": self.code_lines[line_num - 1].strip(),
            }
            
            return True, description
        
        return False, "Not Available"

    def apply_fixes_from_report(self, report_path: str, file_path: str):
        """Reads the report and applies all 'Prepared' fixes to the source file."""
        if not os.path.exists(report_path):
            print(f"Error: Report file not found at {report_path}.")
            return

        with open(report_path, 'r', encoding='utf-8') as f:
            report_data = json.load(f)

        issues_to_fix = [
            issue for issue in report_data.get('issues', []) 
            if issue.get('autofix_status') == 'Prepared' and 'fix_patch' in issue
        ]
        
        if not issues_to_fix:
            print("No auto-fixable issues found in the report.")
            return

        print(f"Applying {len(issues_to_fix)} fixes to {file_path}...")

        # Read the original file content
        with open(file_path, 'r', encoding='utf-8') as f:
            content_lines = f.readlines()

        # Group fixes by type (we only handle MagicNumber here)
        magic_number_fixes = [
            issue['fix_patch'] for issue in issues_to_fix 
            if issue['type'] == 'MagicNumber'
        ]

        # 1. Prepare constant definitions for MagicNumber fixes
        new_constants = []
        for fix in magic_number_fixes:
            new_constants.append(f"{fix['constant_name']} = {fix['constant_value']}\n")
            
        # 2. Insert constants at the top of the file (after imports/docstrings, simple for now)
        # Find the line to insert (usually after the first line or first import)
        insertion_point = 0
        if content_lines:
             # Skip empty lines or docstrings to find a good insertion point
            for i, line in enumerate(content_lines):
                if line.strip() and not line.strip().startswith(('"""', "'''")):
                    insertion_point = i
                    break
        
        # Insert a constant block
        content_lines.insert(insertion_point, "# --- AUTO-GENERATED CONSTANTS ---\n")
        for constant_line in reversed(new_constants):
            content_lines.insert(insertion_point + 1, constant_line)
        content_lines.insert(insertion_point + len(new_constants) + 1, "# --------------------------------\n\n")

        # 3. Apply line replacements (from bottom up to preserve line numbers)
        for fix in sorted(magic_number_fixes, key=lambda x: x['line_to_replace'], reverse=True):
            line_index = fix['line_to_replace'] - 1
            old_line = content_lines[line_index]
            new_line = old_line.replace(str(fix['constant_value']), fix['constant_name'])
            content_lines[line_index] = new_line
            print(f"  -> Applied fix for L{fix['line_to_replace']}: Replaced '{fix['constant_value']}' with '{fix['constant_name']}'")


        # 4. Write the modified content back to the file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.writelines(content_lines)

        print(f"\n✅ All {len(issues_to_fix)} fixes applied successfully to {file_path}.")