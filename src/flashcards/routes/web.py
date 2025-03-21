from fastapi import APIRouter, Request, Form, HTTPException, Depends
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from typing import Optional, Dict, Any

from src.flashcards.database import csv_db
from src.flashcards.ai import gemini
from src.flashcards.utils.template_helper import get_common_context

# Create web router with no prefix (for root routes)
router = APIRouter(tags=["web"])

# Define templates
templates = Jinja2Templates(directory="app/templates")

# Routes
@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Homepage showing all flashcards"""
    flashcards = csv_db.get_flashcards()
    context = get_common_context()
    context["nav_info"]["current_path"] = "/"
    context["flashcards"] = flashcards.to_dict('records')
    
    return templates.TemplateResponse("index.html", {"request": request, **context})

@router.get("/create", response_class=HTMLResponse)
async def create_get(request: Request):
    """Flashcard creation page"""
    context = get_common_context()
    context["nav_info"]["current_path"] = "/create"
    return templates.TemplateResponse("create.html", {"request": request, **context})

@router.post("/create")
async def create_post(
    request: Request,
    word: str = Form(...),
    language: str = Form("english")
):
    """Handle flashcard creation form submission"""
    if not word.strip():
        context = get_common_context()
        context["nav_info"]["current_path"] = "/create"
        return templates.TemplateResponse(
            "create.html", 
            {"request": request, **context, "error": "Please enter a word"}
        )
    
    try:
        # Use Gemini to generate flashcard content
        flashcard_data = await gemini.generate_flashcard_data(word, language)
        
        csv_db.save_flashcard(
            word=word,
            language=language,
            translations=flashcard_data['translations'],
            pronunciation=flashcard_data['pronunciation'],
            examples=flashcard_data['examples']
        )
        
        return RedirectResponse(url="/", status_code=303)
    except Exception as e:
        context = get_common_context()
        context["nav_info"]["current_path"] = "/create"
        return templates.TemplateResponse(
            "create.html", 
            {"request": request, **context, "error": f"Error creating flashcard: {str(e)}"}
        )

@router.get("/edit/{flashcard_id}", response_class=HTMLResponse)
async def edit_get(request: Request, flashcard_id: int):
    """Flashcard edit page"""
    flashcard = csv_db.get_flashcard(flashcard_id)
    if not flashcard:
        return RedirectResponse(url="/", status_code=303)
    
    context = get_common_context()
    context["nav_info"]["current_path"] = f"/edit/{flashcard_id}"
    context["flashcard"] = flashcard
    
    return templates.TemplateResponse("edit.html", {"request": request, **context})

@router.post("/edit/{flashcard_id}")
async def edit_post(
    request: Request,
    flashcard_id: int,
    word: str = Form(...),
    language: str = Form("english"),
    translations: str = Form(""),
    pronunciation: str = Form(""),
    examples: str = Form("")
):
    """Handle flashcard edit form submission"""
    if not word.strip():
        flashcard = csv_db.get_flashcard(flashcard_id)
        
        context = get_common_context()
        context["nav_info"]["current_path"] = f"/edit/{flashcard_id}"
        context["flashcard"] = flashcard
        context["error"] = "Please enter a word"
        
        return templates.TemplateResponse("edit.html", {"request": request, **context})
    
    csv_db.save_flashcard(
        word=word,
        language=language,
        translations=translations,
        pronunciation=pronunciation,
        examples=examples,
        flashcard_id=flashcard_id
    )
    
    return RedirectResponse(url="/", status_code=303)

@router.post("/delete/{flashcard_id}")
async def delete(flashcard_id: int):
    """Delete a flashcard"""
    csv_db.delete_flashcard(flashcard_id)
    return RedirectResponse(url="/", status_code=303)

@router.get("/study", response_class=HTMLResponse)
async def study(request: Request):
    """Study page for flashcards"""
    flashcards = csv_db.get_flashcards()
    
    context = get_common_context()
    context["nav_info"]["current_path"] = "/study"
    context["flashcards"] = flashcards.to_dict('records')
    
    return templates.TemplateResponse("study.html", {"request": request, **context}) 