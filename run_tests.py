#!/usr/bin/env python
"""
Test runner for StudyWAI application

This script runs the tests for the StudyWAI application. You can run it directly
or use pytest directly with specific test files.

Usage:
    python run_tests.py            # Run all tests
    python run_tests.py --api      # Run only API tests
    python run_tests.py --all      # Run both pytest and request-based tests
"""

import os
import sys
import subprocess
from rich.console import Console

console = Console()

def run_pytest_tests():
    """Run tests using pytest"""
    console.print("\n[bold blue]Running tests with pytest...[/bold blue]")
    
    # Run pytest with -v for verbose output and --no-header to hide pytest header
    result = subprocess.run(["pytest", "-v", "tests/"], capture_output=False)
    
    if result.returncode == 0:
        console.print("[bold green]✓ All pytest tests passed![/bold green]")
        return True
    else:
        console.print("[bold red]✗ Some pytest tests failed.[/bold red]")
        return False

def run_feature_tests():
    """Run integration tests using direct requests"""
    console.print("\n[bold blue]Running feature tests with direct HTTP requests...[/bold blue]")
    
    import test_all_features
    test_all_features.run_all_tests()
    
    return True  # The function handles its own result printing

def main():
    """Run the specified tests based on command line arguments"""
    console.print("[bold yellow]================================[/bold yellow]")
    console.print("[bold yellow]  StudyWAI Application Tests  [/bold yellow]")
    console.print("[bold yellow]================================[/bold yellow]")
    
    # Parse command line arguments
    if len(sys.argv) > 1:
        if sys.argv[1] == "--api":
            run_pytest_tests()
        elif sys.argv[1] == "--all":
            run_pytest_tests()
            run_feature_tests()
        else:
            console.print("[bold red]Unknown option. Use --api or --all.[/bold red]")
    else:
        # Default behavior: run pytest tests
        run_pytest_tests()
    
    console.print("\n[bold]Testing completed![/bold]")

if __name__ == "__main__":
    # Make sure we're in the right directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    main() 