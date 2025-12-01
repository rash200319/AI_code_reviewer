# ai-code-reviewer/core/report/json_reporter.py
import json
from typing import List, Dict, Any

def generate_report(issues: List[Dict[str, Any]], filename: str) -> Dict[str, Any]:
    """
    Creates a structured dictionary report from a list of issues.
    """
    report = {
        "metadata": {
            "file": filename,
            "total_issues": len(issues),
            "tool_version": "0.1.0" 
        },
        "issues": issues
    }
    return report

def write_json_report(report_data: Dict[str, Any], output_path: str):
    """
    Writes the report data to a JSON file.
    """
    try:
        # 'w' mode for writing, 'utf-8' encoding for compatibility
        with open(output_path, 'w', encoding='utf-8') as f:
            # Use indent=4 for clean, human-readable JSON output
            json.dump(report_data, f, indent=4)
        print(f"  ✅ Report written successfully to: {output_path}")
    except IOError as e:
        print(f"  ❌ Error writing report file: {e}")
        