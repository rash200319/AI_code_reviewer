# ai-code-reviewer/cli/main.py (FINAL WEEK 2 VERSION)
import click 
import os
from typing import List, Dict, Any

# --- CORE IMPORTS ---
from core.parser.python_parser import PythonParser
from core.detectors.magic_number_detector import MagicNumberDetector
from core.report.json_reporter import generate_report, write_json_report
# --- NEW LLM IMPORT ---
from core.llm.suggestion_generator import SuggestionGenerator
# ----------------------

import sys
import os

# Correct path to venv site-packages
venv_site = os.path.join(os.path.dirname(sys.executable), "..", "Lib", "site-packages")
venv_site = os.path.abspath(venv_site)

if venv_site not in sys.path:
    sys.path.insert(0, venv_site)

print("Python sys.path after fix:", sys.path)



@click.command()
@click.argument('path', type=click.Path(exists=True))
@click.option('--output', '-o', default='code_reviewer_report.json', 
              type=click.Path(), help='Path to output JSON report.')
def analyze(path: str, output: str):
    """
    The main CLI entrypoint for the AI Code Reviewer.
    Analyzes a Python file or directory for code smells.
    """
    if os.path.isdir(path):
        click.echo(f"Directory analysis is not yet implemented. Please specify a file.")
        return

    try:
        all_issues: List[Dict[str, Any]] = []

        click.echo(f"\n🚀 Starting analysis for: {path}")
        
        # 1. File Loader
        code = PythonParser.load_code(path)
        click.echo("  ✅ File loaded.")

        # 2. AST Parser
        tree = PythonParser.parse_ast(code)
        click.echo("  ✅ AST generated.")
        
        # Initialize LLM generator ONCE
        llm_generator = SuggestionGenerator()

        # --- CODE SMELL DETECTION & ENRICHMENT ---
        click.echo("\n🚨 Code Smell Detection & AI Enrichment:")
        
        # Magic Number Detector
        detector = MagicNumberDetector()
        detector.visit(tree)
        
        # Iterate over detected issues to enrich with AI
        for issue in detector.get_issues():
            click.echo(f"  🧠 Requesting AI suggestion for L{issue['line']}...")
            
            # Generate the suggestion using the LLM
            suggestion = llm_generator.generate_suggestion(issue, code)
            
            # Add the suggestion to the issue object
            issue['suggestion'] = suggestion 
            all_issues.append(issue)
        
        # Summary
        if all_issues:
            click.echo(f"  🛑 Found and enriched {len(all_issues)} total issue(s).")
            # Detailed output with suggestion preview
            for issue in all_issues:
                click.echo(f"    [L{issue['line']}] {issue['type']}: {issue['message']}")
                click.echo(f"      AI Suggestion: {issue['suggestion'][:60].replace('\n', ' ')}...")
        else:
            click.echo("  ✨ No issues found.")

        # --- REPORT GENERATION ---
        click.echo("\n📑 Generating Report:")
        # Ensure the output directory exists
        os.makedirs(os.path.dirname(output) or '.', exist_ok=True)
        report_data = generate_report(all_issues, filename=path)
        write_json_report(report_data, output)

    except Exception as e:
        click.echo(f"\n❌ An error occurred during analysis: {e}")

if __name__ == '__main__':
    analyze()# ai-code-reviewer/cli/main.py (Updated with --fix flag)
import argparse
import json
import os
from core.analysis.analyzer import Analyzer
from core.llm.suggestion_generator import SuggestionGenerator
from core.autofix.fixer import Fixer # Make sure this import is present

REPORT_PATH = "code_reviewer_report.json"

def main():
    parser = argparse.ArgumentParser(description="AI Code Reviewer Tool")
    parser.add_argument("file_path", type=str, help="Path to the Python file to analyze.")
    # New argument for applying fixes
    parser.add_argument("--fix", action="store_true", help="Apply all prepared fixes from the latest report.")
    
    args = parser.parse_args()
    file_path = args.file_path

    if not os.path.exists(file_path):
        print(f"Error: File not found at {file_path}")
        return

    # --- AUTO-FIX MODE ---
    if args.fix:
        # We only need the Fixer here, not the Analyzer or LLM
        # Read file content for the Fixer (needed for line management)
        with open(file_path, 'r', encoding='utf-8') as f:
            code = f.read()
            
        fixer = Fixer(code)
        fixer.apply_fixes_from_report(REPORT_PATH, file_path)
        return

    # --- ANALYSIS MODE (Original Logic) ---
    print("\n🚨 Starting AI Code Review...")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        code = f.read()
        
    analyzer = Analyzer(code)
    issues = analyzer.analyze()
    
    if not issues:
        print("🎉 No code smells found!")
        return

    # Initialize LLM and Fixer
    llm_generator = SuggestionGenerator()
    fixer = Fixer(code)
    
    print(f"\n🚨 Code Smell Detection & AI Enrichment: Found {len(issues)} issue(s)...")

    for i, issue in enumerate(issues):
        # 1. Generate AI Suggestion
        print(f"  🧠 Requesting AI suggestion for L{issue['line']}...")
        issue['suggestion'] = llm_generator.generate_suggestion(issue, code)
        
        # 2. Generate Fix Data
        fix_success, fix_description = fixer.generate_fix(issue)
        if fix_success:
            issue['autofix_status'] = "Prepared"
            issue['autofix_description'] = fix_description
        else:
            issue['autofix_status'] = "Not Available"
            issue['autofix_description'] = "Automatic fix not supported for this issue type."

    print(f"  🛑 Found and enriched {len(issues)} total issue(s).")
    for issue in issues:
        print(f"    [L{issue['line']}] {issue['type']}: Fix Status: {issue['autofix_status']}")

    # --- Generate Final Report ---
    report = {
        "metadata": {
            "file": file_path,
            "total_issues": len(issues),
            "tool_version": "0.1.0"
        },
        "issues": issues
    }

    print(f"\n📑 Generating Report:")
    try:
        with open(REPORT_PATH, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=4)
        print(f"  ✅ Report written successfully to: {REPORT_PATH}")
    except Exception as e:
        print(f"  ❌ Error writing report: {e}")

if __name__ == "__main__":
    main()