from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
import os
import logging
import json

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import our modules
from src.flashcards.database import csv_db
from src.flashcards.routes import api
from src.flashcards.ai import gemini
from src.flashcards.utils.template_helper import get_common_context

# Initialize FastAPI app
app = FastAPI(title="StudyWAI - AI-Powered Flashcard Application")

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

# Initialize database
csv_db.init_database()

# Include API router
app.include_router(api.router)

# Define web routes directly in app.py
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Homepage showing all flashcards"""
    flashcards = csv_db.get_flashcards()
    context = get_common_context()
    context["nav_info"]["current_path"] = "/"
    context["flashcards"] = flashcards.to_dict('records')
    
    return templates.TemplateResponse("index.html", {"request": request, **context})

@app.get("/create", response_class=HTMLResponse)
async def create_get(request: Request):
    """Flashcard creation page"""
    context = get_common_context()
    context["nav_info"]["current_path"] = "/create"
    return templates.TemplateResponse("create.html", {"request": request, **context})

@app.post("/create")
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

@app.get("/edit/{flashcard_id}", response_class=HTMLResponse)
async def edit_get(request: Request, flashcard_id: int):
    """Flashcard edit page"""
    flashcard = csv_db.get_flashcard(flashcard_id)
    if not flashcard:
        return RedirectResponse(url="/", status_code=303)
    
    context = get_common_context()
    context["nav_info"]["current_path"] = f"/edit/{flashcard_id}"
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

@app.post("/delete/{flashcard_id}")
async def delete(flashcard_id: int, request: Request):
    """Delete a flashcard"""
    try:
        # Check if flashcard exists first
        flashcard = csv_db.get_flashcard(flashcard_id)
        if not flashcard:
            # Return a JSON response for API clients or redirect with message for browser
            if request.headers.get('content-type') == 'application/json':
                return JSONResponse(
                    content={"error": f"Flashcard with ID {flashcard_id} not found"},
                    status_code=404
                )
            else:
                return RedirectResponse(
                    url=f"/?error=Flashcard+with+ID+{flashcard_id}+not+found", 
                    status_code=303
                )
                
        # Delete the flashcard
        csv_db.delete_flashcard(flashcard_id)
        
        # Return appropriate response based on request type
        if request.headers.get('content-type') == 'application/json':
            return JSONResponse(
                content={"success": True, "message": "Flashcard deleted successfully"}, 
                status_code=200
            )
        else:
            return RedirectResponse(
                url="/?success=Flashcard+deleted+successfully", 
                status_code=303
            )
    except Exception as e:
        logger.error(f"Error deleting flashcard {flashcard_id}: {str(e)}")
        
        # Return appropriate error response based on request type
        if request.headers.get('content-type') == 'application/json':
            return JSONResponse(
                content={"error": f"Failed to delete flashcard: {str(e)}"}, 
                status_code=500
            )
        else:
            return RedirectResponse(
                url=f"/?error=Failed+to+delete+flashcard:+{str(e)}", 
                status_code=303
            )

@app.get("/delete/{flashcard_id}")
async def delete_get(flashcard_id: int, request: Request):
    """Handle GET requests to delete endpoint and redirect with error message"""
    # Return a redirect with an error message
    if request.headers.get('accept') and 'text/html' in request.headers.get('accept'):
        return RedirectResponse(
            url=f"/?error=Please+use+the+delete+button+on+the+card.+Direct+GET+requests+to+delete+are+not+allowed.",
            status_code=303
        )
    else:
        return JSONResponse(
            content={"error": "DELETE method required for this endpoint. GET is not supported."},
            status_code=405
        )

@app.get("/study", response_class=HTMLResponse)
async def study(request: Request):
    """Study page for flashcards"""
    flashcards = csv_db.get_flashcards()
    
    context = get_common_context()
    context["nav_info"]["current_path"] = "/study"
    context["flashcards"] = flashcards.to_dict('records')
    
    return templates.TemplateResponse("study.html", {"request": request, **context})

# AI Tools Routes
@app.get("/grammar", response_class=HTMLResponse)
async def grammar_check(request: Request):
    """Grammar Check tool page"""
    context = get_common_context()
    context["nav_info"]["current_path"] = "/grammar"
    return templates.TemplateResponse("grammar.html", {"request": request, **context})

@app.get("/translate", response_class=HTMLResponse)
async def translate(request: Request):
    """Translation tool page"""
    context = get_common_context()
    context["nav_info"]["current_path"] = "/translate"
    return templates.TemplateResponse("translate.html", {"request": request, **context})

@app.get("/summarize", response_class=HTMLResponse)
async def summarize(request: Request):
    """Summarize tool page"""
    context = get_common_context()
    context["nav_info"]["current_path"] = "/summarize"
    return templates.TemplateResponse("summarize.html", {"request": request, **context})

@app.get("/chatbot", response_class=HTMLResponse)
async def chatbot(request: Request):
    """Chatbot Assistant page"""
    context = get_common_context()
    context["nav_info"]["current_path"] = "/chatbot"
    
    # Get recent chat history
    context["chat_history"] = csv_db.get_chat_history(5)
    
    return templates.TemplateResponse("chatbot.html", {"request": request, **context})

@app.post("/api/chat")
async def api_chat(request: Request):
    """API endpoint for chatbot interaction"""
    try:
        data = await request.json()
        message = data.get("message", "")
        context = data.get("context", "")
        
        if not message:
            return JSONResponse(
                content={"error": "No message provided"}, 
                status_code=400
            )
        
        # Use the chat_with_ai function from gemini
        response = await gemini.chat_with_ai(message, context)
        
        return JSONResponse(content={"response": response})
    except Exception as e:
        logger.error(f"Error in chat API: {str(e)}")
        return JSONResponse(
            content={"error": f"Failed to process request: {str(e)}"}, 
            status_code=500
        )

@app.get("/api/history/{feature}")
async def api_history(feature: str, limit: int = 10):
    """Get history of interactions for a specific feature"""
    try:
        history = csv_db.get_query_log(feature, limit)
        return JSONResponse(content={"history": history})
    except Exception as e:
        logger.error(f"Error getting history: {str(e)}")
        return JSONResponse(
            content={"error": f"Failed to retrieve history: {str(e)}"}, 
            status_code=500
        )

@app.get("/healthcheck")
async def healthcheck():
    """Simple health check endpoint"""
    return {"status": "healthy"}

# Run the app with uvicorn when this file is executed directly
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=1912, reload=True) 