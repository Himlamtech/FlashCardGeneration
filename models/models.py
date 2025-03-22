from sqlalchemy import Column, String, DateTime, Integer, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship
from database.database import Base
import datetime

class Flashcard(Base):
    __tablename__ = "flashcards"
    
    id = Column(String, primary_key=True, index=True)
    word = Column(String, index=True)
    language = Column(String, index=True)
    translations = Column(String)
    pronunciation = Column(String, nullable=True)
    examples = Column(Text)
    created_at = Column(DateTime, default=datetime.datetime.now)
    updated_at = Column(DateTime, nullable=True)
    
    # Study tracking
    times_studied = Column(Integer, default=0)
    times_correct = Column(Integer, default=0)
    last_studied = Column(DateTime, nullable=True)
    
    # Related entities
    tags = relationship("FlashcardTag", back_populates="flashcard")
    study_records = relationship("StudyRecord", back_populates="flashcard")
    
class Tag(Base):
    __tablename__ = "tags"
    
    id = Column(String, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    
    # Related entities
    flashcards = relationship("FlashcardTag", back_populates="tag")
    
class FlashcardTag(Base):
    __tablename__ = "flashcard_tags"
    
    flashcard_id = Column(String, ForeignKey("flashcards.id"), primary_key=True)
    tag_id = Column(String, ForeignKey("tags.id"), primary_key=True)
    
    # Relationships
    flashcard = relationship("Flashcard", back_populates="tags")
    tag = relationship("Tag", back_populates="flashcards")
    
class StudyRecord(Base):
    __tablename__ = "study_records"
    
    id = Column(String, primary_key=True, index=True)
    flashcard_id = Column(String, ForeignKey("flashcards.id"))
    studied_at = Column(DateTime, default=datetime.datetime.now)
    was_correct = Column(Boolean, default=False)
    
    # Relationships
    flashcard = relationship("Flashcard", back_populates="study_records")
    
class StudySession(Base):
    __tablename__ = "study_sessions"
    
    id = Column(String, primary_key=True, index=True)
    start_time = Column(DateTime, default=datetime.datetime.now)
    end_time = Column(DateTime, nullable=True)
    cards_studied = Column(Integer, default=0)
    cards_correct = Column(Integer, default=0)
    
class TranslationHistory(Base):
    __tablename__ = "translation_history"
    
    id = Column(String, primary_key=True, index=True)
    source_text = Column(Text)
    translated_text = Column(Text)
    source_language = Column(String)
    target_language = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.now)
    
class UserSetting(Base):
    __tablename__ = "user_settings"
    
    id = Column(String, primary_key=True, default="default")
    daily_goal = Column(Integer, default=10)
    study_streak = Column(Integer, default=0)
    last_streak_date = Column(DateTime, nullable=True)
    theme = Column(String, default="light")
    preferred_languages = Column(String, default="") 