from fastapi import APIRouter, HTTPException
from typing import List

from src.flashcards.models.schemas import (
    TextRequest,
    TranslationRequest,
    GrammarResponse,
    TranslationResponse,
    SummaryResponse
)
from src.flashcards.ai import gemini

# Create API router
router = APIRouter(prefix="/api")

@router.post("/check-grammar", response_model=GrammarResponse)
async def check_grammar(request: TextRequest):
    """Check grammar for given text"""
    if not request.text:
        raise HTTPException(status_code=400, detail="No text provided")
    
    try:
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
        result = await gemini.translate(request.text, request.source_lang, request.target_lang)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/summarize", response_model=SummaryResponse)
async def summarize(request: TextRequest):
    """Summarize text"""
    if not request.text:
        raise HTTPException(status_code=400, detail="No text provided")
    
    try:
        result = await gemini.summarize(request.text)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 