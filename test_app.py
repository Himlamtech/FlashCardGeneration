import requests
import time
import random
import string
import os

BASE_URL = "http://localhost:5000"

def test_homepage():
    """Test the homepage is working"""
    response = requests.get(f"{BASE_URL}/")
    assert response.status_code == 200
    print("✅ Homepage is working")

def test_create_page():
    """Test the create flashcard page is working"""
    response = requests.get(f"{BASE_URL}/create")
    assert response.status_code == 200
    print("✅ Create page is working")

def test_study_page():
    """Test the study page is working"""
    response = requests.get(f"{BASE_URL}/study")
    assert response.status_code == 200
    print("✅ Study page is working")

def test_grammar_page():
    """Test the grammar check page is working"""
    response = requests.get(f"{BASE_URL}/grammar")
    assert response.status_code == 200
    print("✅ Grammar check page is working")

def test_translate_page():
    """Test the translation page is working"""
    response = requests.get(f"{BASE_URL}/translate")
    assert response.status_code == 200
    print("✅ Translation page is working")

def test_summarize_page():
    """Test the summarize page is working"""
    response = requests.get(f"{BASE_URL}/summarize")
    assert response.status_code == 200
    print("✅ Summarize page is working")

def test_chatbot_page():
    """Test the chatbot page is working"""
    response = requests.get(f"{BASE_URL}/chatbot")
    assert response.status_code == 200
    print("✅ Chatbot page is working")

def test_health_check():
    """Test the health check endpoint is working"""
    response = requests.get(f"{BASE_URL}/healthcheck")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
    print("✅ Health check is working")

def run_all_tests():
    """Run all tests"""
    print("🔍 Running tests for StudyWAI application...")
    print("-" * 50)
    
    tests = [
        test_homepage,
        test_create_page,
        test_study_page,
        test_grammar_page,
        test_translate_page,
        test_summarize_page,
        test_chatbot_page,
        test_health_check
    ]
    
    successful_tests = 0
    for test in tests:
        try:
            test()
            successful_tests += 1
        except Exception as e:
            print(f"❌ {test.__name__} failed: {str(e)}")
    
    print("-" * 50)
    print(f"✅ {successful_tests}/{len(tests)} tests passed")

if __name__ == "__main__":
    run_all_tests() 