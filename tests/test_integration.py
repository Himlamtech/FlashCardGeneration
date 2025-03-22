import pytest
from fastapi.testclient import TestClient

def test_create_and_study_workflow(client):
    """Test the complete workflow of creating a flashcard and studying it"""
    
    # 1. Create a flashcard
    create_data = {
        "word": "bonjour",
        "language": "french",
        "translations": "hello, hi, good day",
        "pronunciation": "bɔ̃ʒuʁ",
        "examples": "Bonjour, comment ça va?|Bonjour tout le monde!|Il m'a dit bonjour ce matin."
    }
    
    response = client.post(
        "/create",
        data=create_data,
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    
    # Should redirect to home page
    assert response.status_code == 303
    
    # 2. Visit home page and check if the flashcard is there
    response = client.get("/")
    assert response.status_code == 200
    assert "bonjour" in response.text
    
    # 3. Visit study page
    response = client.get("/study")
    assert response.status_code == 200
    assert "Study Flashcards" in response.text
    
def test_ai_feature_workflow(client):
    """Test the AI-powered features workflow"""
    
    # 1. Test translation
    translate_data = {
        "text": "Hello, how are you?",
        "source_lang": "english",
        "target_lang": "spanish"
    }
    
    response = client.post("/api/translate", json=translate_data)
    assert response.status_code == 200
    result = response.json()
    assert "translated_text" in result
    
    # 2. Test grammar check
    grammar_data = {
        "text": "This sentence have an error.",
        "language": "english",
        "check_types": ["grammar", "spelling"]
    }
    
    response = client.post("/api/grammar-check", json=grammar_data)
    assert response.status_code == 200
    result = response.json()
    assert "overall_score" in result
    
    # 3. Test summarization
    summarize_data = {
        "text": "This is a long text that needs to be summarized. It contains multiple sentences with various information. The goal is to extract the most important points and create a concise summary that captures the essential information.",
        "length": "short",
        "style": "paragraph"
    }
    
    response = client.post("/api/summarize", json=summarize_data)
    assert response.status_code == 200
    result = response.json()
    assert "summary" in result
    
    # 4. Test chatbot
    chat_data = {
        "messages": [
            {"role": "user", "content": "How can I improve my vocabulary?"}
        ]
    }
    
    response = client.post("/api/chat", json=chat_data)
    assert response.status_code == 200
    result = response.json()
    assert "response" in result

def test_error_handling(client):
    """Test error handling in the API endpoints"""
    
    # 1. Test with invalid data for translation
    invalid_data = {
        "text": "Hello",
        # Missing required fields
    }
    
    response = client.post("/api/translate", json=invalid_data)
    assert response.status_code in [400, 422]  # 422 is FastAPI's default validation error
    
    # 2. Test with non-existent flashcard ID
    response = client.get("/edit/non-existent-id")
    assert response.status_code == 404
    
    # 3. Test delete with non-existent flashcard ID
    response = client.post("/delete/non-existent-id")
    assert response.status_code == 404 