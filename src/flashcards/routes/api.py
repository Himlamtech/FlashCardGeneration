from fastapi import APIRouter, HTTPException
from typing import List, Optional

from src.flashcards.models.schemas import (
    TextRequest,
    TranslationRequest,
    SummarizeRequest,
    GrammarResponse,
    TranslationResponse,
    SummaryResponse
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
        result = await gemini.check_grammar(request.text)
        
        # Save to grammar history database
        csv_db.save_grammar_history(request.text, result.get("corrected_text", ""))
        
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
        
        result = await gemini.translate(
            request.text, 
            source_lang, 
            target_lang
        )
        
        # Save to translation history database
        csv_db.save_translation_history(
            request.text,
            result.get("translated_text", ""),
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
        
        result = await gemini.summarize(
            request.text,
            length,
            style
        )
        
        # Save to summarize history database
        csv_db.save_summarize_history(
            request.text,
            result.get("summary", ""),
            length,
            style
        )
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 