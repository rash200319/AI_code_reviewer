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
    analyze()