from fastapi import APIRouter, HTTPException
from typing import List, Optional

from src.flashcards.models.schemas import (
    TextRequest,
    TranslationRequest,
    SummarizeRequest,
    GrammarResponse,
    TranslationResponse,
    SummaryResponse,
    ChatRequest,
    ChatResponse
)
from src.flashcards.ai import gemini
from src.flashcards.database import csv_db

# Create API router
router = APIRouter(prefix="/api")

@router.post("/check-grammar", response_model=GrammarResponse)
async def check_grammar(request: TextRequest):
    """Check grammar for given text"""
    if not request.text:
        raise HTTPException(status_code=400, detail="No text provided")
    
    try:
        # The gemini.check_grammar function now handles database logging internally
        result = await gemini.check_grammar(request.text)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/translate", response_model=TranslationResponse)
async def translate(request: TranslationRequest):
    """Translate text from source language to target language"""
    if not request.text:
        raise HTTPException(status_code=400, detail="No text provided")
    
    try:
        source_lang = request.source_lang or "auto"
        target_lang = request.target_lang or "en"
        
        # The gemini.translate function now handles database logging internally
        result = await gemini.translate(
            request.text, 
            source_lang, 
            target_lang
        )
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/summarize", response_model=SummaryResponse)
async def summarize(request: SummarizeRequest):
    """Summarize text"""
    if not request.text:
        raise HTTPException(status_code=400, detail="No text provided")
    
    try:
        length = request.length or "medium"
        style = request.style or "informative"
        
        # The gemini.summarize function now handles database logging internally
        result = await gemini.summarize(
            request.text,
            length,
            style
        )
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Chat with AI assistant"""
    if not request.message:
        raise HTTPException(status_code=400, detail="No message provided")
    
    try:
        # The chat_with_ai function handles database logging internally
        response = await gemini.chat_with_ai(
            request.message,
            request.context
        )
        
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/history/{feature}")
async def get_history(feature: str, limit: int = 10):
    """Get history of interactions for a specific feature"""
    try:
        history = csv_db.get_query_log(feature, limit)
        return {"history": history}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 