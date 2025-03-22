import re
import json
from datetime import datetime
import uuid
import hashlib

def generate_unique_id():
    """Generate a unique ID for database entities"""
    return str(uuid.uuid4())

def sanitize_input(text):
    """Clean user input to prevent potential security issues"""
    if not text:
        return ""
    # Remove any HTML/script tags
    text = re.sub(r'<[^>]*>', '', text)
    return text.strip()

def parse_json_safely(json_string):
    """Safely parse JSON from AI responses"""
    try:
        # First try to parse directly
        return json.loads(json_string)
    except json.JSONDecodeError:
        # If that fails, try to find a JSON object in the string
        json_match = re.search(r'(\{.*\})', json_string, re.DOTALL)
        if json_match:
            try:
                return json.loads(json_match.group(1))
            except json.JSONDecodeError:
                pass
        
        # If all else fails, return an empty dict
        return {}

def format_datetime(dt, format_string="%Y-%m-%d %H:%M"):
    """Format a datetime object into a readable string"""
    if isinstance(dt, str):
        try:
            dt = datetime.fromisoformat(dt)
        except ValueError:
            return dt
    
    if isinstance(dt, datetime):
        return dt.strftime(format_string)
    
    return ""

def calculate_study_progress(correct, total):
    """Calculate and format study progress percentage"""
    if total == 0:
        return "0%"
    
    percentage = (correct / total) * 100
    return f"{int(percentage)}%"

def get_progress_color(correct, total):
    """Get appropriate Bootstrap color class based on study progress"""
    if total == 0:
        return "secondary"
    
    percentage = (correct / total) * 100
    
    if percentage < 30:
        return "danger"
    elif percentage < 70:
        return "warning"
    else:
        return "success"

def truncate_text(text, max_length=100):
    """Truncate text to specified length and add ellipsis if needed"""
    if not text:
        return ""
    
    if len(text) <= max_length:
        return text
    
    return text[:max_length].rstrip() + "..."

def extract_keywords(text, max_keywords=5):
    """Simple keyword extraction from text (placeholder for more sophisticated algorithm)"""
    if not text:
        return []
    
    # Remove common words and punctuation, split by spaces
    text = re.sub(r'[^\w\s]', '', text.lower())
    words = text.split()
    
    # Remove common English stop words
    stop_words = {
        "a", "an", "the", "and", "or", "but", "if", "then", "else", "when",
        "at", "from", "by", "with", "about", "against", "between", "into",
        "through", "during", "before", "after", "above", "below", "to", "from",
        "up", "down", "in", "out", "on", "off", "over", "under", "again",
        "further", "then", "once", "here", "there", "when", "where", "why",
        "how", "all", "any", "both", "each", "few", "more", "most", "other",
        "some", "such", "no", "nor", "not", "only", "own", "same", "so", "than",
        "too", "very", "s", "t", "can", "will", "just", "don", "should", "now",
        "i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you",
        "your", "yours", "yourself", "yourselves", "he", "him", "his", "himself",
        "she", "her", "hers", "herself", "it", "its", "itself", "they", "them",
        "their", "theirs", "themselves", "what", "which", "who", "whom", "this",
        "that", "these", "those", "am", "is", "are", "was", "were", "be", "been",
        "being", "have", "has", "had", "having", "do", "does", "did", "doing",
        "would", "should", "could", "ought", "i'm", "you're", "he's", "she's",
        "it's", "we're", "they're", "i've", "you've", "we've", "they've", "i'd",
        "you'd", "he'd", "she'd", "we'd", "they'd", "i'll", "you'll", "he'll",
        "she'll", "we'll", "they'll", "isn't", "aren't", "wasn't", "weren't",
        "hasn't", "haven't", "hadn't", "doesn't", "don't", "didn't", "won't",
        "wouldn't", "shan't", "shouldn't", "can't", "cannot", "couldn't", "mustn't",
        "let's", "that's", "who's", "what's", "here's", "there's", "when's",
        "where's", "why's", "how's"
    }
    
    filtered_words = [word for word in words if word not in stop_words and len(word) > 3]
    
    # Count word frequencies
    word_freq = {}
    for word in filtered_words:
        if word in word_freq:
            word_freq[word] += 1
        else:
            word_freq[word] = 1
    
    # Sort by frequency and return top keywords
    sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
    return [word for word, freq in sorted_words[:max_keywords]]

def generate_password_hash(password):
    """Generate a secure hash for a password"""
    salt = uuid.uuid4().hex
    return hashlib.sha256(salt.encode() + password.encode()).hexdigest() + ':' + salt

def check_password_hash(hashed_password, user_password):
    """Verify a password against its hash"""
    password, salt = hashed_password.split(':')
    return password == hashlib.sha256(salt.encode() + user_password.encode()).hexdigest() 