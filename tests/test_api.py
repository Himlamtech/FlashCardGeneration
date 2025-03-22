import pytest
from fastapi.testclient import TestClient
from app.app import app

client = TestClient(app)

def test_homepage():
    """Test that the homepage returns a 200 status code"""
    response = client.get("/")
    assert response.status_code == 200
    assert "StudyWAI" in response.text

def test_create_page():
    """Test that the create page loads correctly"""
    response = client.get("/create")
    assert response.status_code == 200
    assert "Create Flashcard" in response.text

def test_study_page():
    """Test that the study page loads correctly"""
    response = client.get("/study")
    assert response.status_code == 200
    assert "Study Flashcards" in response.text

def test_translate_api():
    """Test the translation API endpoint"""
    test_data = {
        "text": "Hello world",
        "source_lang": "english",
        "target_lang": "spanish"
    }
    response = client.post("/api/translate", json=test_data)
    assert response.status_code == 200
    result = response.json()
    assert "translated_text" in result
    assert result["source_lang"] == "english"
    assert result["target_lang"] == "spanish"

def test_grammar_check_api():
    """Test the grammar check API endpoint"""
    test_data = {
        "text": "This sentence have an error.",
        "language": "english",
        "check_types": ["grammar", "spelling"]
    }
    response = client.post("/api/grammar-check", json=test_data)
    assert response.status_code == 200
    result = response.json()
    assert "overall_score" in result
    assert "issues" in result
    assert "improved_text" in result

def test_summarize_api():
    """Test the summarize API endpoint"""
    test_data = {
        "text": "This is a long text that needs to be summarized. It contains multiple sentences with various information. The goal is to extract the most important points and create a concise summary that captures the essential information.",
        "length": "short",
        "style": "paragraph"
    }
    response = client.post("/api/summarize", json=test_data)
    assert response.status_code == 200
    result = response.json()
    assert "summary" in result
    assert "topics" in result
    assert "terms" in result
    assert result["style"] == "paragraph" 