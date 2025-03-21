import requests
import json
import os
from rich import print
from rich.console import Console
from rich.table import Table

console = Console()

# Base URL for the API
BASE_URL = "http://127.0.0.1:5000"

def test_feature(feature_name, test_func):
    """Run a test function and print the result"""
    console.print(f"\n[bold blue]Testing {feature_name}...[/bold blue]")
    
    try:
        result = test_func()
        if result:
            console.print(f"[bold green]✓ {feature_name} test passed![/bold green]")
            return True
        else:
            console.print(f"[bold red]✗ {feature_name} test failed![/bold red]")
            return False
    except Exception as e:
        console.print(f"[bold red]✗ {feature_name} test failed with error: {str(e)}[/bold red]")
        return False

def test_home_page():
    """Test home page accessibility"""
    response = requests.get(f"{BASE_URL}/")
    return response.status_code == 200

def test_create_page():
    """Test create page accessibility"""
    response = requests.get(f"{BASE_URL}/create")
    return response.status_code == 200

def test_study_page():
    """Test study page accessibility"""
    response = requests.get(f"{BASE_URL}/study")
    return response.status_code == 200

def test_flashcard_creation():
    """Test flashcard creation"""
    # Disable automatic redirect following to properly check for 303 status
    response = requests.post(
        f"{BASE_URL}/create",
        data={"word": "test_word", "language": "english"},
        allow_redirects=False
    )
    console.print(f"Flashcard creation status code: {response.status_code}")
    return response.status_code == 303  # Redirect after creation

def test_grammar_check():
    """Test grammar check API"""
    response = requests.post(
        f"{BASE_URL}/api/check-grammar",
        json={"text": "This is a test sentense with an error."}
    )
    if response.status_code != 200:
        return False
    
    data = response.json()
    return "corrected_text" in data and "errors" in data

def test_translation():
    """Test translation API"""
    response = requests.post(
        f"{BASE_URL}/api/translate",
        json={
            "text": "Hello, how are you?",
            "source_lang": "english",
            "target_lang": "french"
        }
    )
    if response.status_code != 200:
        return False
    
    data = response.json()
    return "translated_text" in data

def test_summarization():
    """Test summarization API"""
    long_text = """
    The Python programming language is an interpreted, high-level, general-purpose programming language.
    Created by Guido van Rossum and first released in 1991, Python's design philosophy emphasizes code 
    readability with its notable use of significant whitespace. Its language constructs and object-oriented 
    approach aim to help programmers write clear, logical code for small and large-scale projects.
    Python is dynamically typed and garbage-collected. It supports multiple programming paradigms, 
    including structured (particularly, procedural), object-oriented, and functional programming.
    """
    
    response = requests.post(
        f"{BASE_URL}/api/summarize",
        json={"text": long_text}
    )
    if response.status_code != 200:
        return False
    
    data = response.json()
    return "summary" in data

def run_all_tests():
    """Run all tests and print a summary"""
    tests = [
        ("Home Page", test_home_page),
        ("Create Page", test_create_page),
        ("Study Page", test_study_page),
        ("Flashcard Creation", test_flashcard_creation),
        ("Grammar Check API", test_grammar_check),
        ("Translation API", test_translation),
        ("Summarization API", test_summarization)
    ]
    
    results = []
    for name, test_func in tests:
        result = test_feature(name, test_func)
        results.append((name, result))
    
    # Print summary table
    console.print("\n[bold]Test Results Summary:[/bold]")
    table = Table(show_header=True)
    table.add_column("Feature", style="cyan")
    table.add_column("Status", style="magenta")
    
    passed = 0
    for name, result in results:
        status = "[green]PASSED[/green]" if result else "[red]FAILED[/red]"
        table.add_row(name, status)
        if result:
            passed += 1
    
    console.print(table)
    console.print(f"\n[bold]Tests passed: {passed}/{len(results)}[/bold]")

if __name__ == "__main__":
    console.print("[bold yellow]Testing All Features of Flash Card Generation App[/bold yellow]")
    console.print(f"[italic]Connecting to {BASE_URL}[/italic]")
    run_all_tests() 