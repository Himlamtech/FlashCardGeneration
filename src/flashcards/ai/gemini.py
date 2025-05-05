import os
import json
import re
import google.generativeai as genai
from dotenv import load_dotenv
from src.flashcards.database import csv_db

# Load environment variables
load_dotenv()

# Initialize Gemini API
gemini_api_key = os.getenv('GEMINI_API_KEY')
if not gemini_api_key:
    gemini_api_key = os.getenv('GOOGLE_AI_API_KEY')  # Try alternative name
    
if not gemini_api_key:
    raise ValueError("No Gemini API key found. Please set GEMINI_API_KEY or GOOGLE_AI_API_KEY in .env file")

genai.configure(api_key=gemini_api_key)
model = genai.GenerativeModel('gemini-pro')  # Updated to use latest model

async def generate_flashcard_data(word, language):
    """
    Generate flashcard data for a given word using Gemini AI
    """
    prompt = f"""
    Generate flashcard data for the {language} word: "{word}"
    
    Return your response in the following JSON format:
    {{
        "translations": "comma-separated list of translations",
        "pronunciation": "phonetic pronunciation",
        "examples": "3 example sentences using the word, separated by semicolons"
    }}
    
    Only respond with the JSON, no other text.
    """
    
    response = model.generate_content(prompt)
    response_text = response.text
    
    # Process response to extract the JSON
    try:
        # Try to parse as JSON directly
        try:
            data = json.loads(response_text)
        except:
            # If direct parsing fails, try to extract JSON using regex
            json_match = re.search(r'\{[^}]*"translations"[^}]*"pronunciation"[^}]*"examples"[^}]*\}', response_text, re.DOTALL)
            if json_match:
                try:
                    data = json.loads(json_match.group(0))
                except:
                    # Fallback to manual extraction
                    data = {
                        "translations": "No translations available",
                        "pronunciation": "No pronunciation available",
                        "examples": "No examples available"
                    }
            else:
                # Manual extraction
                translations_match = re.search(r'"translations"\s*:\s*"([^"]*)"', response_text)
                pronunciation_match = re.search(r'"pronunciation"\s*:\s*"([^"]*)"', response_text)
                examples_match = re.search(r'"examples"\s*:\s*"([^"]*)"', response_text)
                
                data = {
                    "translations": translations_match.group(1) if translations_match else "No translations available",
                    "pronunciation": pronunciation_match.group(1) if pronunciation_match else "No pronunciation available",
                    "examples": examples_match.group(1) if examples_match else "No examples available"
                }
    except Exception as e:
        print(f"Error parsing Gemini response: {e}")
        data = {
            "translations": "Error retrieving translations",
            "pronunciation": "Error retrieving pronunciation",
            "examples": "Error retrieving examples"
        }
    
    # Log the query and response
    query = f"Generate flashcard for '{word}' in {language}"
    response_str = json.dumps(data)
    csv_db.save_query_log("flashcard_generation", query, response_str)
        
    return data

async def check_grammar(text):
    """
    Check grammar for given text using Gemini AI
    """
    prompt = f"""
    Check the grammar of the following text and provide corrections:
    
    "{text}"
    
    Return your response in the following JSON format:
    {{
        "corrected_text": "text with corrections",
        "errors": "list of errors found, separated by semicolons"
    }}
    
    Only respond with the JSON, no other text.
    """
    
    response = model.generate_content(prompt)
    response_text = response.text
    
    try:
        # Try to parse as JSON directly
        try:
            data = json.loads(response_text)
        except:
            # If direct parsing fails, try to extract JSON using regex
            json_match = re.search(r'\{[^}]*"corrected_text"[^}]*"errors"[^}]*\}', response_text, re.DOTALL)
            if json_match:
                try:
                    data = json.loads(json_match.group(0))
                except:
                    # Fallback to manual extraction
                    corrected_match = re.search(r'"corrected_text"\s*:\s*"([^"]*)"', response_text)
                    errors_match = re.search(r'"errors"\s*:\s*"([^"]*)"', response_text)
                    
                    data = {
                        "corrected_text": corrected_match.group(1) if corrected_match else text,
                        "errors": errors_match.group(1) if errors_match else "No errors found"
                    }
            else:
                data = {
                    "corrected_text": text,
                    "errors": "Could not analyze text"
                }
    except Exception as e:
        data = {
            "corrected_text": text,
            "errors": f"Error analyzing text: {str(e)}"
        }
    
    # Save to grammar history database and log
    csv_db.save_grammar_history(text, data.get("corrected_text", ""))
        
    return data

async def translate(text, source_lang, target_lang):
    """
    Translate text from source language to target language using Gemini AI
    """
    prompt = f"""
    Translate the following {source_lang} text to {target_lang}:
    
    "{text}"
    
    Return your response in the following JSON format:
    {{
        "translated_text": "the translation"
    }}
    
    Only respond with the JSON, no other text.
    """
    
    response = model.generate_content(prompt)
    response_text = response.text
    
    try:
        # Try to parse as JSON directly
        try:
            data = json.loads(response_text)
        except:
            # If direct parsing fails, try to extract JSON using regex
            json_match = re.search(r'\{[^}]*"translated_text"[^}]*\}', response_text, re.DOTALL)
            if json_match:
                try:
                    data = json.loads(json_match.group(0))
                except:
                    # Fallback to manual extraction
                    translated_match = re.search(r'"translated_text"\s*:\s*"([^"]*)"', response_text)
                    
                    data = {
                        "translated_text": translated_match.group(1) if translated_match else "Translation failed"
                    }
            else:
                data = {
                    "translated_text": "Translation failed"
                }
    except Exception as e:
        data = {
            "translated_text": f"Error translating text: {str(e)}"
        }
    
    # Save to translation history database
    csv_db.save_translation_history(
        text, 
        data.get("translated_text", ""), 
        source_lang, 
        target_lang
    )
        
    return data

async def summarize(text, length=None, style=None):
    """
    Summarize text using Gemini AI
    
    Args:
        text (str): The text to summarize
        length (str): "short", "medium", or "long"
        style (str): "informative", "academic", or "simplified"
    """
    # Define length parameters
    length_desc = {
        "short": "a very concise summary (1-2 sentences)",
        "medium": "a moderate length summary (3-5 sentences)",
        "long": "a comprehensive summary (multiple paragraphs)"
    }
    
    # Define style parameters
    style_desc = {
        "informative": "factual and informative",
        "academic": "formal academic style",
        "simplified": "simplified language for easier understanding"
    }
    
    length_param = length_desc.get(length, length_desc["medium"]) if length else length_desc["medium"]
    style_param = style_desc.get(style, style_desc["informative"]) if style else style_desc["informative"]
    
    prompt = f"""
    Summarize the following text into {length_param} using a {style_param} style:
    
    "{text}"
    
    Return your response in the following JSON format:
    {{
        "summary": "the summary of the text"
    }}
    
    Only respond with the JSON, no other text.
    """
    
    response = model.generate_content(prompt)
    response_text = response.text
    
    try:
        # Try to parse as JSON directly
        try:
            data = json.loads(response_text)
        except:
            # If direct parsing fails, try to extract JSON using regex
            json_match = re.search(r'\{[^}]*"summary"[^}]*\}', response_text, re.DOTALL)
            if json_match:
                try:
                    data = json.loads(json_match.group(0))
                except:
                    # Fallback to manual extraction
                    summary_match = re.search(r'"summary"\s*:\s*"([^"]*)"', response_text)
                    
                    data = {
                        "summary": summary_match.group(1) if summary_match else "Summarization failed"
                    }
            else:
                data = {
                    "summary": "Summarization failed"
                }
    except Exception as e:
        data = {
            "summary": f"Error summarizing text: {str(e)}"
        }
    
    # Save to summarize history database
    csv_db.save_summarize_history(
        text,
        data.get("summary", ""),
        length or "medium",
        style or "informative"
    )
        
    return data

async def chat_with_ai(message, context=None):
    """
    Chat with the AI assistant
    
    Args:
        message (str): User message
        context (str, optional): Additional context
    """
    prompt = f"""
    You are an AI language learning assistant for the StudyWAI flashcard application.
    
    {context or ""}
    
    User: {message}
    
    Response:
    """
    
    response = model.generate_content(prompt)
    response_text = response.text
    
    # Log the chat conversation
    csv_db.save_chat_history(message, response_text)
    
    return response_text 