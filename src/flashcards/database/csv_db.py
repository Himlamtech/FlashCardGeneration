import os
import csv
import pandas as pd
from datetime import datetime

# Data paths
FLASHCARDS_CSV = 'app/data/flashcards.csv'

# Ensure data directory and files exist
def init_database():
    """Initialize the database files and directories"""
    os.makedirs('app/data', exist_ok=True)
    if not os.path.exists(FLASHCARDS_CSV):
        with open(FLASHCARDS_CSV, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['id', 'word', 'language', 'translations', 'pronunciation', 'examples', 'created_at', 'updated_at'])

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