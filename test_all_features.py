import requests
import json
import os
import time
from rich import print
from rich.console import Console
from rich.table import Table

console = Console()

# Base URL for the API
BASE_URL = "http://127.0.0.1:8000"

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

def test_flashcard_deletion():
    """Test flashcard deletion"""
    # First, create a flashcard with a unique word to identify it
    unique_word = f"delete_test_{int(time.time())}"
    create_response = requests.post(
        f"{BASE_URL}/create",
        data={"word": unique_word, "language": "english"},
        allow_redirects=False
    )
    
    if create_response.status_code != 303:
        console.print(f"Setup failed: Could not create test flashcard. Status: {create_response.status_code}")
        return False
    
    # Get the home page to find the flashcard ID
    home_response = requests.get(f"{BASE_URL}/")
    
    if home_response.status_code != 200:
        console.print("Setup failed: Could not retrieve home page")
        return False
    
    # Simple check to see if our unique word is in the page
    if unique_word not in home_response.text:
        console.print("Setup failed: Could not find created flashcard on home page")
        return False
    
    # Extract the flashcard ID from the page (this is a simple approach)
    # In a real test, you might want to use a more robust method like parsing the HTML
    # For now, we'll just look for the ID in the delete form
    import re
    match = re.search(r'/delete/([a-f0-9\-]+)"', home_response.text)
    
    if not match:
        console.print("Setup failed: Could not extract flashcard ID")
        return False
    
    flashcard_id = match.group(1)
    
    # Now delete the flashcard
    delete_response = requests.post(
        f"{BASE_URL}/delete/{flashcard_id}",
        allow_redirects=False
    )
    
    console.print(f"Flashcard deletion status code: {delete_response.status_code}")
    return delete_response.status_code == 303  # Redirect after deletion

def test_flashcard_edit():
    """Test flashcard editing"""
    # First, create a flashcard with a unique word to identify it
    unique_word = f"edit_test_{int(time.time())}"
    create_response = requests.post(
        f"{BASE_URL}/create",
        data={"word": unique_word, "language": "english"},
        allow_redirects=False
    )
    
    if create_response.status_code != 303:
        console.print(f"Setup failed: Could not create test flashcard. Status: {create_response.status_code}")
        return False
    
    # Get the home page to find the flashcard ID
    home_response = requests.get(f"{BASE_URL}/")
    
    if home_response.status_code != 200:
        console.print("Setup failed: Could not retrieve home page")
        return False
    
    # Extract the flashcard ID from the page (simple approach)
    import re
    match = re.search(r'/edit/([a-f0-9\-]+)"', home_response.text)
    
    if not match:
        console.print("Setup failed: Could not extract flashcard ID")
        return False
    
    flashcard_id = match.group(1)
    
    # Edit the flashcard
    edit_response = requests.post(
        f"{BASE_URL}/edit/{flashcard_id}",
        data={
            "word": "edited_word",
            "language": "english",
            "translations": "translation1, translation2",
            "pronunciation": "pronunciation_test",
            "examples": "example sentence"
        },
        allow_redirects=False
    )
    
    console.print(f"Flashcard edit status code: {edit_response.status_code}")
    return edit_response.status_code == 303  # Redirect after edit

def test_grammar_check():
    """Test grammar check API"""
    response = requests.post(
        f"{BASE_URL}/api/grammar-check",
        json={
            "text": "This is a test sentense with an error.",
            "language": "english",
            "check_types": ["grammar", "spelling"]
        }
    )
    if response.status_code != 200:
        return False
    
    data = response.json()
    return "improved_text" in data and "issues" in data

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
        json={
            "text": long_text,
            "length": "medium",
            "style": "paragraph"
        }
    )
    if response.status_code != 200:
        return False
    
    data = response.json()
    return "summary" in data

def test_summarization_with_params():
    """Test summarization API with custom length and style"""
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
        json={
            "text": long_text,
            "length": "short",
            "style": "bullet"
        }
    )
    if response.status_code != 200:
        return False
    
    data = response.json()
    return "summary" in data

def test_grammar_page():
    """Test grammar page accessibility"""
    response = requests.get(f"{BASE_URL}/grammar")
    return response.status_code == 200

def test_translate_page():
    """Test translate page accessibility"""
    response = requests.get(f"{BASE_URL}/translate")
    return response.status_code == 200

def test_summarize_page():
    """Test summarize page accessibility"""
    response = requests.get(f"{BASE_URL}/summarize")
    return response.status_code == 200

def test_chatbot_page():
    """Test chatbot page accessibility"""
    response = requests.get(f"{BASE_URL}/chatbot")
    return response.status_code == 200

def test_healthcheck():
    """Test the health check endpoint"""
    response = requests.get(f"{BASE_URL}/healthcheck")
    if response.status_code != 200:
        return False
    
    data = response.json()
    return data["status"] == "healthy"

def test_chat_api():
    """Test the chat API endpoint"""
    response = requests.post(
        f"{BASE_URL}/api/chat",
        json={
            "messages": [
                {"role": "user", "content": "How can I improve my vocabulary?"}
            ]
        }
    )
    if response.status_code != 200:
        return False
    
    data = response.json()
    return "response" in data

def run_all_tests():
    """Run all application tests and print a summary"""
    console.print("\n[bold yellow]======================================[/bold yellow]")
    console.print("[bold yellow]  Running StudyWAI Application Tests  [/bold yellow]")
    console.print("[bold yellow]======================================[/bold yellow]")
    
    tests = [
        ("Home Page", test_home_page),
        ("Create Page", test_create_page),
        ("Study Page", test_study_page),
        ("Grammar Page", test_grammar_page),
        ("Translate Page", test_translate_page),
        ("Summarize Page", test_summarize_page),
        ("Chatbot Page", test_chatbot_page),
        ("Flashcard Creation", test_flashcard_creation),
        ("Flashcard Editing", test_flashcard_edit),
        ("Flashcard Deletion", test_flashcard_deletion),
        ("Grammar Check API", test_grammar_check),
        ("Translation API", test_translation),
        ("Summarization API", test_summarization),
        ("Summarization with Parameters", test_summarization_with_params),
        ("Health Check Endpoint", test_healthcheck),
        ("Chat API", test_chat_api)
    ]
    
    results = {}
    
    for name, test_func in tests:
        results[name] = test_feature(name, test_func)
        
    # Create a summary table
    table = Table(title="Test Results Summary")
    table.add_column("Test", style="cyan")
    table.add_column("Result", style="magenta")
    
    passed = 0
    total = len(tests)
    
    for name, result in results.items():
        status = "[green]PASSED[/green]" if result else "[red]FAILED[/red]"
        table.add_row(name, status)
        if result:
            passed += 1
    
    console.print("\n")
    console.print(table)
    
    console.print(f"\n[bold]Overall Progress: {passed}/{total} tests passed ({int(passed/total*100)}%)[/bold]")
    
    if passed == total:
        console.print("\n[bold green]✓ All tests passed successfully![/bold green]")
    else:
        console.print(f"\n[bold yellow]⚠ {total-passed} tests failed. See above for details.[/bold yellow]")

if __name__ == "__main__":
    run_all_tests() 