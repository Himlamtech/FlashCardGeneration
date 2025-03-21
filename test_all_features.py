import requests
import json
import os
import shutil
from rich import print
from rich.console import Console
from rich.table import Table

console = Console()

# Base URL for the API
BASE_URL = "http://127.0.0.1:5000"

def reset_database():
    """Reset the application databases before testing"""
    console.print("\n[bold yellow]Resetting test databases...[/bold yellow]")
    try:
        # Create data directory if it doesn't exist
        os.makedirs('app/data', exist_ok=True)
        
        # Database files to reset
        db_files = [
            'flashcards.csv',
            'grammar_history.csv',
            'translate_history.csv',
            'summarize_history.csv'
        ]
        
        # Backup and reset each database file
        for db_file in db_files:
            file_path = f'app/data/{db_file}'
            
            # Backup existing database if it exists
            if os.path.exists(file_path):
                backup_path = f'{file_path}.bak'
                shutil.copy(file_path, backup_path)
                console.print(f"Backed up existing database to {backup_path}")
            
            # Create empty database file with headers
            with open(file_path, 'w', newline='', encoding='utf-8') as f:
                if db_file == 'flashcards.csv':
                    f.write('id,word,language,translations,pronunciation,examples,created_at,updated_at\n')
                elif db_file == 'grammar_history.csv':
                    f.write('id,original_text,corrected_text,created_at\n')
                elif db_file == 'translate_history.csv':
                    f.write('id,original_text,source_lang,target_lang,translated_text,created_at\n')
                elif db_file == 'summarize_history.csv':
                    f.write('id,original_text,summary,length,style,created_at\n')
        
        console.print("[bold green]✓ Databases reset successful![/bold green]")
        return True
    except Exception as e:
        console.print(f"[bold red]✗ Database reset failed: {str(e)}[/bold red]")
        return False

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
    # First, create a flashcard
    create_response = requests.post(
        f"{BASE_URL}/create",
        data={"word": "delete_test", "language": "english"},
        allow_redirects=False
    )
    
    if create_response.status_code != 303:
        console.print(f"Setup failed: Could not create test flashcard. Status: {create_response.status_code}")
        return False
    
    # Get the list of flashcards to find the ID
    home_response = requests.get(f"{BASE_URL}/")
    if home_response.status_code != 200:
        console.print("Setup failed: Could not retrieve flashcards")
        return False
    
    # Now delete using POST method (not GET)
    # This assumes there's at least one flashcard with ID 1
    delete_response = requests.post(
        f"{BASE_URL}/delete/1",
        allow_redirects=False
    )
    
    console.print(f"Flashcard deletion status code: {delete_response.status_code}")
    return delete_response.status_code == 303  # Redirect after deletion

def test_flashcard_edit():
    """Test flashcard editing"""
    # First, create a flashcard
    create_response = requests.post(
        f"{BASE_URL}/create",
        data={"word": "edit_test", "language": "english"},
        allow_redirects=False
    )
    
    if create_response.status_code != 303:
        console.print(f"Setup failed: Could not create test flashcard. Status: {create_response.status_code}")
        return False
    
    # Edit the flashcard
    # This assumes there's at least one flashcard with ID 1
    edit_response = requests.post(
        f"{BASE_URL}/edit/1",
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
            "style": "academic"
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
    """Test healthcheck endpoint"""
    response = requests.get(f"{BASE_URL}/healthcheck")
    if response.status_code != 200:
        return False
    
    data = response.json()
    return data.get("status") == "healthy"

def test_grammar_history_record():
    """Test that grammar check history is saved to database"""
    # Make a grammar check API call first
    test_grammar_check()
    
    # Check if the history was recorded in the database
    try:
        import pandas as pd
        df = pd.read_csv('app/data/grammar_history.csv')
        return not df.empty and 'corrected_text' in df.columns and len(df) > 0
    except Exception as e:
        console.print(f"Error reading grammar history: {str(e)}")
        return False

def test_translation_history_record():
    """Test that translation history is saved to database"""
    # Make a translation API call first
    test_translation()
    
    # Check if the history was recorded in the database
    try:
        import pandas as pd
        df = pd.read_csv('app/data/translate_history.csv')
        return not df.empty and 'translated_text' in df.columns and len(df) > 0
    except Exception as e:
        console.print(f"Error reading translation history: {str(e)}")
        return False

def test_summarize_history_record():
    """Test that summarization history is saved to database"""
    # Make a summarization API call first
    test_summarization()
    
    # Check if the history was recorded in the database
    try:
        import pandas as pd
        df = pd.read_csv('app/data/summarize_history.csv')
        return not df.empty and 'summary' in df.columns and len(df) > 0
    except Exception as e:
        console.print(f"Error reading summarization history: {str(e)}")
        return False

def run_all_tests():
    """Run all tests and print a summary"""
    # First, reset the database
    if not reset_database():
        console.print("[bold red]Database reset failed. Tests may not run properly.[/bold red]")
    
    tests = [
        ("Home Page", test_home_page),
        ("Create Page", test_create_page),
        ("Study Page", test_study_page),
        ("Grammar Page", test_grammar_page),
        ("Translate Page", test_translate_page),
        ("Summarize Page", test_summarize_page),
        ("Chatbot Page", test_chatbot_page),
        ("Flashcard Creation", test_flashcard_creation),
        ("Flashcard Deletion", test_flashcard_deletion),
        ("Flashcard Edit", test_flashcard_edit),
        ("Grammar Check API", test_grammar_check),
        ("Translation API", test_translation),
        ("Summarization API", test_summarization),
        ("Summarization API with Parameters", test_summarization_with_params),
        ("Health Check", test_healthcheck),
        ("Grammar History Recording", test_grammar_history_record),
        ("Translation History Recording", test_translation_history_record),
        ("Summarization History Recording", test_summarize_history_record)
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