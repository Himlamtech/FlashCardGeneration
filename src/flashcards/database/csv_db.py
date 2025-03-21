import os
import csv
import pandas as pd
from datetime import datetime

# Data paths
DATA_DIR = 'app/data'
FLASHCARDS_CSV = os.path.join(DATA_DIR, 'flashcards.csv')
GRAMMAR_HISTORY_CSV = os.path.join(DATA_DIR, 'grammar_history.csv')
TRANSLATE_HISTORY_CSV = os.path.join(DATA_DIR, 'translate_history.csv')
SUMMARIZE_HISTORY_CSV = os.path.join(DATA_DIR, 'summarize_history.csv')

# Ensure data directory and files exist
def init_database():
    """Initialize the database files and directories"""
    os.makedirs(DATA_DIR, exist_ok=True)
    
    # Initialize flashcards database
    if not os.path.exists(FLASHCARDS_CSV):
        with open(FLASHCARDS_CSV, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['id', 'word', 'language', 'translations', 'pronunciation', 'examples', 'created_at', 'updated_at'])
    
    # Initialize grammar check history
    if not os.path.exists(GRAMMAR_HISTORY_CSV):
        with open(GRAMMAR_HISTORY_CSV, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['id', 'original_text', 'corrected_text', 'created_at'])
    
    # Initialize translation history
    if not os.path.exists(TRANSLATE_HISTORY_CSV):
        with open(TRANSLATE_HISTORY_CSV, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['id', 'original_text', 'source_lang', 'target_lang', 'translated_text', 'created_at'])
    
    # Initialize summarization history
    if not os.path.exists(SUMMARIZE_HISTORY_CSV):
        with open(SUMMARIZE_HISTORY_CSV, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['id', 'original_text', 'summary', 'length', 'style', 'created_at'])

def get_flashcards():
    """Get all flashcards from the CSV database"""
    try:
        return pd.read_csv(FLASHCARDS_CSV)
    except:
        return pd.DataFrame(columns=['id', 'word', 'language', 'translations', 'pronunciation', 'examples', 'created_at', 'updated_at'])

def save_flashcard(word, language, translations, pronunciation, examples, flashcard_id=None):
    """Save a flashcard to the CSV database"""
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
    """Delete a flashcard from the CSV database"""
    df = get_flashcards()
    if int(flashcard_id) in df['id'].values:
        df = df[df['id'] != int(flashcard_id)]
        df.to_csv(FLASHCARDS_CSV, index=False)
        return True
    return False

def get_flashcard(flashcard_id):
    """Get a specific flashcard by ID"""
    df = get_flashcards()
    if int(flashcard_id) in df['id'].values:
        return df[df['id'] == int(flashcard_id)].to_dict('records')[0]
    return None

# Grammar check history functions
def save_grammar_history(original_text, corrected_text):
    """Save grammar check history to CSV database"""
    try:
        df = pd.read_csv(GRAMMAR_HISTORY_CSV)
    except:
        df = pd.DataFrame(columns=['id', 'original_text', 'corrected_text', 'created_at'])
    
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    new_id = 1 if df.empty else df['id'].max() + 1
    
    new_row = {
        'id': new_id,
        'original_text': original_text[:500],  # Limit text length
        'corrected_text': corrected_text[:500],  # Limit text length
        'created_at': now
    }
    
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df.to_csv(GRAMMAR_HISTORY_CSV, index=False)
    return True

# Translation history functions
def save_translation_history(original_text, translated_text, source_lang, target_lang):
    """Save translation history to CSV database"""
    try:
        df = pd.read_csv(TRANSLATE_HISTORY_CSV)
    except:
        df = pd.DataFrame(columns=['id', 'original_text', 'source_lang', 'target_lang', 'translated_text', 'created_at'])
    
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    new_id = 1 if df.empty else df['id'].max() + 1
    
    new_row = {
        'id': new_id,
        'original_text': original_text[:500],  # Limit text length
        'source_lang': source_lang,
        'target_lang': target_lang,
        'translated_text': translated_text[:500],  # Limit text length
        'created_at': now
    }
    
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df.to_csv(TRANSLATE_HISTORY_CSV, index=False)
    return True

# Summarization history functions
def save_summarize_history(original_text, summary, length, style):
    """Save summarization history to CSV database"""
    try:
        df = pd.read_csv(SUMMARIZE_HISTORY_CSV)
    except:
        df = pd.DataFrame(columns=['id', 'original_text', 'summary', 'length', 'style', 'created_at'])
    
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    new_id = 1 if df.empty else df['id'].max() + 1
    
    new_row = {
        'id': new_id,
        'original_text': original_text[:500],  # Limit text length
        'summary': summary[:500],  # Limit text length
        'length': length or 'medium',
        'style': style or 'informative',
        'created_at': now
    }
    
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df.to_csv(SUMMARIZE_HISTORY_CSV, index=False)
    return True 