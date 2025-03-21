from fastapi import FastAPI, Request, Form, HTTPException, Depends
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional, List, Dict, Any
import os
import csv
import json
import re
import pandas as pd
from dotenv import load_dotenv
import google.generativeai as genai
from datetime import datetime
from pydantic import BaseModel

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(title="Flash Card Generation using AI")

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Set up templates
templates = Jinja2Templates(directory="app/templates")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Gemini API
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
model = genai.GenerativeModel('gemini-2.0-flash-lite-001')

# Data paths
FLASHCARDS_CSV = 'app/data/flashcards.csv'

# Ensure data directory and files exist
os.makedirs('app/data', exist_ok=True)
if not os.path.exists(FLASHCARDS_CSV):
    with open(FLASHCARDS_CSV, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['id', 'word', 'language', 'translations', 'pronunciation', 'examples', 'created_at', 'updated_at'])

# Pydantic models for request/response
class TextRequest(BaseModel):
    text: str

class TranslationRequest(BaseModel):
    text: str
    source_lang: str = "english"
    target_lang: str = "vietnamese"

# Helper functions
def get_flashcards():
    try:
        return pd.read_csv(FLASHCARDS_CSV)
    except:
        return pd.DataFrame(columns=['id', 'word', 'language', 'translations', 'pronunciation', 'examples', 'created_at', 'updated_at'])

def save_flashcard(word, language, translations, pronunciation, examples, flashcard_id=None):
    df = get_flashcards()
    
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    if flashcard_id is not None and not pd.isna(flashcard_id) and int(flashcard_id) in df['id'].values:
        # Update existing flashcard
        idx = df.index[df['id'] == int(flashcard_id)].tolist()[0]
        df.at[idx, 'word'] = word
        df.at[idx, 'language'] = language
        df.at[idx, 'translations'] = translations
        df.at[idx, 'pronunciation'] = pronunciation
        df.at[idx, 'examples'] = examples
        df.at[idx, 'updated_at'] = now
    else:
        # Create new flashcard
        new_id = 1 if df.empty else df['id'].max() + 1
        new_row = {
            'id': new_id,
            'word': word,
            'language': language,
            'translations': translations,
            'pronunciation': pronunciation,
            'examples': examples,
            'created_at': now,
            'updated_at': now
        }
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    
    df.to_csv(FLASHCARDS_CSV, index=False)
    return True

def delete_flashcard(flashcard_id):
    df = get_flashcards()
    if int(flashcard_id) in df['id'].values:
        df = df[df['id'] != int(flashcard_id)]
        df.to_csv(FLASHCARDS_CSV, index=False)
        return True
    return False

# Context for templates
def get_common_context():
    return {
        "now": {"year": datetime.now().year},
        "request": {"path": ""}  # Will be updated in routes
    }

# Routes
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    flashcards = get_flashcards()
    context = get_common_context()
    context["request"]["path"] = "/"
    context["flashcards"] = flashcards.to_dict('records')
    
    return templates.TemplateResponse("index.html", {"request": request, **context})

@app.get("/create", response_class=HTMLResponse)
async def create_get(request: Request):
    context = get_common_context()
    context["request"]["path"] = "/create"
    return templates.TemplateResponse("create.html", {"request": request, **context})

@app.post("/create")
async def create_post(
    request: Request,
    word: str = Form(...),
    language: str = Form("english")
):
    if not word.strip():
        context = get_common_context()
        context["request"]["path"] = "/create"
        return templates.TemplateResponse(
            "create.html", 
            {"request": request, **context, "error": "Please enter a word"}
        )
    
    try:
        # Use Gemini to generate flashcard content
        flashcard_data = await generate_flashcard_data(word, language)
        
        save_flashcard(
            word=word,
            language=language,
            translations=flashcard_data['translations'],
            pronunciation=flashcard_data['pronunciation'],
            examples=flashcard_data['examples']
        )
        
        return RedirectResponse(url="/", status_code=303)
    except Exception as e:
        context = get_common_context()
        context["request"]["path"] = "/create"
        return templates.TemplateResponse(
            "create.html", 
            {"request": request, **context, "error": f"Error creating flashcard: {str(e)}"}
        )

@app.get("/edit/{flashcard_id}", response_class=HTMLResponse)
async def edit_get(request: Request, flashcard_id: int):
    df = get_flashcards()
    if int(flashcard_id) not in df['id'].values:
        return RedirectResponse(url="/", status_code=303)
    
    flashcard = df[df['id'] == int(flashcard_id)].to_dict('records')[0]
    
    context = get_common_context()
    context["request"]["path"] = f"/edit/{flashcard_id}"
    context["flashcard"] = flashcard
    
    return templates.TemplateResponse("edit.html", {"request": request, **context})

@app.post("/edit/{flashcard_id}")
async def edit_post(
    request: Request,
    flashcard_id: int,
    word: str = Form(...),
    language: str = Form("english"),
    translations: str = Form(""),
    pronunciation: str = Form(""),
    examples: str = Form("")
):
    if not word.strip():
        df = get_flashcards()
        flashcard = df[df['id'] == int(flashcard_id)].to_dict('records')[0]
        
        context = get_common_context()
        context["request"]["path"] = f"/edit/{flashcard_id}"
        context["flashcard"] = flashcard
        context["error"] = "Please enter a word"
        
        return templates.TemplateResponse("edit.html", {"request": request, **context})
    
    save_flashcard(
        word=word,
        language=language,
        translations=translations,
        pronunciation=pronunciation,
        examples=examples,
        flashcard_id=flashcard_id
    )
    
    return RedirectResponse(url="/", status_code=303)

@app.post("/delete/{flashcard_id}")
async def delete(flashcard_id: int):
    delete_flashcard(flashcard_id)
    return RedirectResponse(url="/", status_code=303)

@app.get("/study", response_class=HTMLResponse)
async def study(request: Request):
    flashcards = get_flashcards()
    
    context = get_common_context()
    context["request"]["path"] = "/study"
    context["flashcards"] = flashcards.to_dict('records')
    
    return templates.TemplateResponse("study.html", {"request": request, **context})

@app.post("/api/check-grammar")
async def check_grammar(request: TextRequest):
    if not request.text:
        raise HTTPException(status_code=400, detail="No text provided")
    
    try:
        result = await check_grammar_with_ai(request.text)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/translate")
async def translate(request: TranslationRequest):
    if not request.text:
        raise HTTPException(status_code=400, detail="No text provided")
    
    try:
        result = await translate_with_ai(request.text, request.source_lang, request.target_lang)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/summarize")
async def summarize(request: TextRequest):
    if not request.text:
        raise HTTPException(status_code=400, detail="No text provided")
    
    try:
        result = await summarize_with_ai(request.text)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# AI Functions using Gemini
async def generate_flashcard_data(word, language):
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
    
    # Process response to extract the JSON
    try:
        response_text = response.text
        
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
        
    return data

async def check_grammar_with_ai(text):
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
    
    try:
        response_text = response.text
        
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
        
    return data

async def translate_with_ai(text, source_lang, target_lang):
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
    
    try:
        response_text = response.text
        
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
        
    return data

async def summarize_with_ai(text):
    prompt = f"""
    Summarize the following text:
    
    "{text}"
    
    Return your response in the following JSON format:
    {{
        "summary": "the summary of the text"
    }}
    
    Only respond with the JSON, no other text.
    """
    
    response = model.generate_content(prompt)
    
    try:
        response_text = response.text
        
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
        
    return data

# Run the application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=5000, reload=True) 