"""
Utilities for working with templates in the StudyWAI application
This module provides helper functions for template rendering
"""

import datetime
import random
from src.flashcards.database import csv_db
import pandas as pd

def get_common_context():
    """
    Get common context variables for all templates
    
    Returns:
        dict: Dictionary with common template variables
    """
    # Get all flashcards to extract languages and stats
    try:
        flashcards_df = csv_db.get_flashcards()
    except Exception:
        flashcards_df = pd.DataFrame(columns=['id', 'word', 'language', 'translations', 'pronunciation', 'examples', 'created_at', 'updated_at'])
    
    # Count languages
    languages = []
    if not flashcards_df.empty and 'language' in flashcards_df.columns:
        languages = flashcards_df['language'].unique().tolist()
    
    # Calculate study streak (simulated for now)
    # In a real app, this would be calculated from user's study history
    study_streak = random.randint(1, 30)
    
    # Navigation info
    nav_info = {
        'current_path': '/',
        'languages': languages,
        'study_streak': study_streak,
        'flashcard_count': len(flashcards_df) if not flashcards_df.empty else 0,
        'dark_mode': False,
        'today': datetime.datetime.now().strftime('%Y-%m-%d'),
    }
    
    return {
        'nav_info': nav_info,
        'debug': False,  # Set to True to enable debug mode
    }

def format_flashcard_for_template(flashcard):
    """
    Format a flashcard dictionary for use in templates
    
    Args:
        flashcard (dict): Flashcard data from database
        
    Returns:
        dict: Formatted flashcard data
    """
    if not flashcard:
        return None
    
    # Ensure all required fields are present
    formatted = {
        'id': flashcard.get('id', 0),
        'word': flashcard.get('word', ''),
        'language': flashcard.get('language', 'english'),
        'translations': flashcard.get('translations', ''),
        'pronunciation': flashcard.get('pronunciation', ''),
        'examples': flashcard.get('examples', ''),
        'created_at': flashcard.get('created_at', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
        'updated_at': flashcard.get('updated_at', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
    }
    
    # Calculate time since creation
    try:
        created_date = datetime.datetime.strptime(formatted['created_at'], '%Y-%m-%d %H:%M:%S')
        now = datetime.datetime.now()
        delta = now - created_date
        
        if delta.days > 0:
            formatted['time_since'] = f"{delta.days} days ago"
        elif delta.seconds // 3600 > 0:
            formatted['time_since'] = f"{delta.seconds // 3600} hours ago"
        else:
            formatted['time_since'] = f"{delta.seconds // 60} minutes ago"
    except Exception:
        formatted['time_since'] = "recently"
    
    return formatted 