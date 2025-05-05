from pydantic import BaseModel
from typing import Optional, List, Dict, Any

class TextRequest(BaseModel):
    """Request model for text-based operations like grammar checking and summarization"""
    text: str

class TranslationRequest(BaseModel):
    """Request model for translation operations"""
    text: str
    source_lang: Optional[str] = None
    target_lang: Optional[str] = None

class SummarizeRequest(BaseModel):
    """Request model for summarization with additional parameters"""
    text: str
    length: Optional[str] = None  # short, medium, long
    style: Optional[str] = None   # informative, academic, simplified

class ChatRequest(BaseModel):
    """Request model for chat with AI assistant"""
    message: str
    context: Optional[str] = None

class FlashcardCreate(BaseModel):
    """Model for flashcard creation"""
    word: str
    language: str = "english"

class FlashcardUpdate(BaseModel):
    """Model for flashcard updates"""
    word: str
    language: str = "english"
    translations: str
    pronunciation: str
    examples: str

class FlashcardResponse(BaseModel):
    """Response model for flashcard data"""
    id: int
    word: str
    language: str
    translations: str
    pronunciation: str
    examples: str
    created_at: str
    updated_at: str

class GrammarResponse(BaseModel):
    """Response model for grammar checking"""
    corrected_text: str
    errors: str

class TranslationResponse(BaseModel):
    """Response model for translation"""
    translated_text: str

class SummaryResponse(BaseModel):
    """Response model for text summarization"""
    summary: str

class ChatResponse(BaseModel):
    """Response model for chat with AI assistant"""
    response: str

class QueryLogEntry(BaseModel):
    """Model for a query log entry"""
    id: int
    feature: str
    query: str
    response: str
    created_at: str

class QueryLogResponse(BaseModel):
    """Response model for query log"""
    history: List[QueryLogEntry] 