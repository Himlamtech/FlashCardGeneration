from fastapi import FastAPI, Request, Form, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import List, Optional, Dict
import os
from dotenv import load_dotenv
import google.generativeai as genai
from database.database import get_db, engine
from models.models import Base, Flashcard
from sqlalchemy.orm import Session
import uuid
from datetime import datetime

# Load environment variables
load_dotenv()

# Setup Gemini AI
genai.configure(api_key=os.getenv("GOOGLE_AI_API_KEY"))
text_model = genai.GenerativeModel('gemini-pro')
vision_model = genai.GenerativeModel('gemini-pro-vision')

# Create database tables
Base.metadata.create_all(bind=engine)

# Create FastAPI app
app = FastAPI()

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Setup templates
templates = Jinja2Templates(directory="app/templates")

# Request models
class TranslateRequest(BaseModel):
    text: str
    source_lang: str
    target_lang: str

class GrammarCheckRequest(BaseModel):
    text: str
    language: str
    check_types: List[str]

class SummarizeRequest(BaseModel):
    text: str
    length: str  # short, medium, long
    style: str   # bullet, paragraph, structured

class ExtractUrlRequest(BaseModel):
    url: str

class ChatRequest(BaseModel):
    messages: List[Dict[str, str]]
    context: Optional[str] = None

# Navigation info for templates
def get_nav_info(request: Request):
    # In a real app, you'd get streak from DB
    study_streak = 5
    
    # Get available languages from flashcards
    db = next(get_db())
    languages = db.query(Flashcard.language).distinct().all()
    languages = [lang[0] for lang in languages]
    
    return {
        "current_path": request.url.path,
        "languages": languages,
        "study_streak": study_streak
    }

# Routes
@app.get("/", response_class=HTMLResponse)
async def home(request: Request, db: Session = Depends(get_db)):
    flashcards = db.query(Flashcard).all()
    return templates.TemplateResponse(
        "index.html", 
        {"request": request, "flashcards": flashcards, "nav_info": get_nav_info(request)}
    )

@app.get("/create", response_class=HTMLResponse)
async def create_form(request: Request):
    return templates.TemplateResponse(
        "create.html", 
        {"request": request, "nav_info": get_nav_info(request)}
    )

@app.post("/create")
async def create_flashcard(
    request: Request,
    word: str = Form(...),
    language: str = Form(...),
    translations: Optional[str] = Form(None),
    pronunciation: Optional[str] = Form(None),
    examples: Optional[str] = Form(None),
    db: Session = Depends(get_db)
):
    # If translations/examples not provided, generate with AI
    if not translations or not examples:
        prompt = f"""
        Create a comprehensive flashcard for the word "{word}" in {language}.
        Include:
        1. Translations (comma separated)
        2. Pronunciation guide
        3. At least 3 example sentences that show proper usage, separated by '|'
        
        Format your answer as a JSON object with these keys:
        - translations
        - pronunciation
        - examples
        """
        response = text_model.generate_content(prompt)
        
        try:
            ai_response = response.text
            # Extract JSON from response - in real app you'd use a proper parser
            import json
            ai_data = json.loads(ai_response)
            
            if not translations:
                translations = ai_data.get("translations", "")
            if not pronunciation:
                pronunciation = ai_data.get("pronunciation", "")
            if not examples:
                examples = ai_data.get("examples", "")
        except Exception as e:
            # Fallback if AI response isn't parseable
            if not translations:
                translations = word
            if not examples:
                examples = f"Example of {word}."
    
    # Create new flashcard
    new_card = Flashcard(
        id=str(uuid.uuid4()),
        word=word,
        language=language,
        translations=translations,
        pronunciation=pronunciation,
        examples=examples,
        created_at=datetime.now()
    )
    
    db.add(new_card)
    db.commit()
    
    return RedirectResponse(url="/", status_code=303)

@app.get("/study", response_class=HTMLResponse)
async def study(request: Request, db: Session = Depends(get_db)):
    flashcards = db.query(Flashcard).all()
    return templates.TemplateResponse(
        "study.html", 
        {"request": request, "flashcards": flashcards, "nav_info": get_nav_info(request)}
    )

@app.get("/edit/{card_id}", response_class=HTMLResponse)
async def edit_form(request: Request, card_id: str, db: Session = Depends(get_db)):
    card = db.query(Flashcard).filter(Flashcard.id == card_id).first()
    if not card:
        raise HTTPException(status_code=404, detail="Flashcard not found")
    
    return templates.TemplateResponse(
        "edit.html", 
        {"request": request, "card": card, "nav_info": get_nav_info(request)}
    )

@app.post("/edit/{card_id}")
async def edit_flashcard(
    request: Request,
    card_id: str,
    word: str = Form(...),
    language: str = Form(...),
    translations: str = Form(...),
    pronunciation: Optional[str] = Form(None),
    examples: str = Form(...),
    db: Session = Depends(get_db)
):
    card = db.query(Flashcard).filter(Flashcard.id == card_id).first()
    if not card:
        raise HTTPException(status_code=404, detail="Flashcard not found")
    
    # Update card
    card.word = word
    card.language = language
    card.translations = translations
    card.pronunciation = pronunciation
    card.examples = examples
    card.updated_at = datetime.now()
    
    db.commit()
    
    return RedirectResponse(url="/", status_code=303)

@app.post("/delete/{card_id}")
async def delete_flashcard(request: Request, card_id: str, db: Session = Depends(get_db)):
    card = db.query(Flashcard).filter(Flashcard.id == card_id).first()
    if not card:
        raise HTTPException(status_code=404, detail="Flashcard not found")
    
    db.delete(card)
    db.commit()
    
    return RedirectResponse(url="/", status_code=303)

@app.get("/translate", response_class=HTMLResponse)
async def translate_page(request: Request):
    return templates.TemplateResponse(
        "translate.html", 
        {"request": request, "nav_info": get_nav_info(request)}
    )

@app.get("/grammar", response_class=HTMLResponse)
async def grammar_page(request: Request):
    return templates.TemplateResponse(
        "grammar.html", 
        {"request": request, "nav_info": get_nav_info(request)}
    )

@app.get("/summarize", response_class=HTMLResponse)
async def summarize_page(request: Request):
    return templates.TemplateResponse(
        "summarize.html", 
        {"request": request, "nav_info": get_nav_info(request)}
    )

@app.get("/chatbot", response_class=HTMLResponse)
async def chatbot_page(request: Request):
    return templates.TemplateResponse(
        "chatbot.html", 
        {"request": request, "nav_info": get_nav_info(request)}
    )

# API Endpoints
@app.post("/api/translate")
async def translate_text(request: TranslateRequest):
    prompt = f"""
    Translate the following text from {request.source_lang} to {request.target_lang}:
    
    {request.text}
    
    Only give me the translation, nothing else.
    """
    
    try:
        response = text_model.generate_content(prompt)
        translated_text = response.text.strip()
        
        return {
            "translated_text": translated_text,
            "source_lang": request.source_lang,
            "target_lang": request.target_lang
        }
    except Exception as e:
        return {"error": str(e)}

@app.post("/api/grammar-check")
async def check_grammar(request: GrammarCheckRequest):
    check_types_str = ", ".join(request.check_types)
    
    prompt = f"""
    Check the following text in {request.language} for {check_types_str} issues:
    
    {request.text}
    
    Please provide:
    1. An overall score out of 100
    2. A list of all issues found, including:
       - severity (error, warning, or suggestion)
       - type (grammar, spelling, style, punctuation)
       - the original text with the issue
       - suggested correction
       - brief explanation
    3. An improved version of the entire text with all issues fixed
    
    Format your response as a JSON object with these keys:
    - overall_score (number)
    - issues (array of objects with severity, type, original, suggestion, explanation)
    - improved_text (string)
    """
    
    try:
        response = text_model.generate_content(prompt)
        
        # In a real application, you would properly parse the JSON response
        # Here we'll just pass it as a simplified example
        import json
        result = json.loads(response.text)
        
        return result
    except Exception as e:
        return {"error": str(e)}

@app.post("/api/summarize")
async def summarize_text(request: SummarizeRequest):
    prompt = f"""
    Summarize the following text in {request.length} length ({request.style} style):
    
    {request.text}
    
    Please provide:
    1. A summary in {request.style} style
    2. A list of main topics discussed
    3. Key terms or vocabulary from the text
    
    Format your response as a JSON object with these keys:
    - summary (string)
    - topics (array of strings)
    - terms (array of strings)
    - style (same as input: {request.style})
    """
    
    try:
        response = text_model.generate_content(prompt)
        
        # In a real application, you would properly parse the JSON response
        import json
        result = json.loads(response.text)
        
        return result
    except Exception as e:
        return {"error": str(e)}

@app.post("/api/extract-url")
async def extract_url_text(request: ExtractUrlRequest):
    prompt = f"""
    Extract the main article text from this URL: {request.url}
    
    Only return the extracted content, nothing else.
    """
    
    try:
        response = text_model.generate_content(prompt)
        content = response.text.strip()
        
        return {
            "content": content,
            "url": request.url
        }
    except Exception as e:
        return {"error": str(e)}

@app.post("/api/chat")
async def chat_with_assistant(request: ChatRequest):
    """Chat with the AI language learning assistant"""
    try:
        # Format context and messages
        context = request.context
        
        # Format messages for Gemini
        formatted_messages = []
        
        # Add context if provided
        if context:
            formatted_messages.append({
                "role": "system",
                "content": f"CONTEXT: {context}\n\nYou are a helpful language learning assistant for StudyWAI."
            })
        else:
            formatted_messages.append({
                "role": "system",
                "content": "You are a helpful language learning assistant for StudyWAI."
            })
        
        # Add user messages
        for msg in request.messages:
            formatted_messages.append(msg)
        
        # Format into prompt for Gemini
        prompt = "\n\n".join([f"{m['role'].upper()}: {m['content']}" for m in formatted_messages])
        response = text_model.generate_content(prompt)
        
        return {
            "response": response.text,
            "messages": request.messages
        }
    except Exception as e:
        return {"error": str(e)}

@app.get("/healthcheck")
async def healthcheck():
    """Health check endpoint for monitoring"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    }

# Startup event
@app.on_event("startup")
async def startup_event():
    print("StudyWAI application starting up...")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.app:app", host="0.0.0.0", port=8000, reload=True) 