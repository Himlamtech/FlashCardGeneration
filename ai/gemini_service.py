import os
import json
from typing import Dict, List, Any, Optional
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GOOGLE_AI_API_KEY"))

# Get models
text_model = genai.GenerativeModel('gemini-pro')
vision_model = genai.GenerativeModel('gemini-pro-vision')

class GeminiService:
    """Service class for interacting with Google's Gemini AI"""
    
    @staticmethod
    async def generate_flashcard(word: str, language: str) -> Dict[str, Any]:
        """Generate a flashcard with translations, pronunciation, and examples for a given word"""
        
        prompt = f"""
        Create a comprehensive flashcard for the word or phrase "{word}" in {language}.
        
        Include:
        1. Translations (comma separated)
        2. Pronunciation guide
        3. At least 3 example sentences that show proper usage, separated by '|'
        
        Format your answer as a JSON object with these keys:
        - translations
        - pronunciation
        - examples
        """
        
        try:
            response = text_model.generate_content(prompt)
            content = response.text
            
            # Parse JSON from response
            # Find JSON object in text (in case model adds additional text)
            import re
            json_match = re.search(r'(\{.*\})', content, re.DOTALL)
            if json_match:
                json_str = json_match.group(1)
                data = json.loads(json_str)
            else:
                data = json.loads(content)
                
            return {
                "translations": data.get("translations", ""),
                "pronunciation": data.get("pronunciation", ""),
                "examples": data.get("examples", "")
            }
        except Exception as e:
            print(f"Error generating flashcard: {str(e)}")
            # Return default values on error
            return {
                "translations": word,
                "pronunciation": "",
                "examples": f"Example of {word}."
            }
    
    @staticmethod
    async def translate_text(text: str, source_lang: str, target_lang: str) -> str:
        """Translate text from source language to target language"""
        
        if source_lang == "auto":
            detect_prompt = f"Detect the language of the following text and respond with only the language name: {text}"
            try:
                detect_response = text_model.generate_content(detect_prompt)
                source_lang = detect_response.text.strip().lower()
            except Exception:
                source_lang = "english"  # Default to English if detection fails
        
        translate_prompt = f"""
        Translate the following text from {source_lang} to {target_lang}:
        
        {text}
        
        Only give me the translation, nothing else.
        """
        
        try:
            response = text_model.generate_content(translate_prompt)
            return response.text.strip()
        except Exception as e:
            print(f"Error translating text: {str(e)}")
            return f"Error: Could not translate text. {str(e)}"
    
    @staticmethod
    async def check_grammar(
        text: str, 
        language: str, 
        check_types: List[str]
    ) -> Dict[str, Any]:
        """Check text for grammar, spelling, style, and punctuation issues"""
        
        check_types_str = ", ".join(check_types)
        
        prompt = f"""
        Check the following text in {language} for {check_types_str} issues:
        
        {text}
        
        Please provide:
        1. An overall score out of 100
        2. A list of all issues found, including:
           - severity (error, warning, or suggestion)
           - type (grammar, spelling, style, punctuation)
           - the original text with the issue
           - suggested correction
           - brief explanation
        3. An improved version of the entire text with all issues fixed
        
        Format your response as a JSON object with these keys:
        - overall_score (number)
        - issues (array of objects with severity, type, original, suggestion, explanation)
        - improved_text (string)
        """
        
        try:
            response = text_model.generate_content(prompt)
            content = response.text
            
            # Parse JSON from response
            import re
            json_match = re.search(r'(\{.*\})', content, re.DOTALL)
            if json_match:
                json_str = json_match.group(1)
                return json.loads(json_str)
            else:
                return json.loads(content)
        except Exception as e:
            print(f"Error checking grammar: {str(e)}")
            return {
                "error": str(e),
                "overall_score": 0,
                "issues": [],
                "improved_text": text
            }
    
    @staticmethod
    async def summarize_text(
        text: str, 
        length: str, 
        style: str
    ) -> Dict[str, Any]:
        """Summarize text to specified length and style"""
        
        prompt = f"""
        Summarize the following text in {length} length ({style} style):
        
        {text}
        
        Please provide:
        1. A summary in {style} style
        2. A list of main topics discussed
        3. Key terms or vocabulary from the text
        
        Format your response as a JSON object with these keys:
        - summary (string)
        - topics (array of strings)
        - terms (array of strings)
        - style (same as input: {style})
        """
        
        try:
            response = text_model.generate_content(prompt)
            content = response.text
            
            # Parse JSON from response
            import re
            json_match = re.search(r'(\{.*\})', content, re.DOTALL)
            if json_match:
                json_str = json_match.group(1)
                return json.loads(json_str)
            else:
                return json.loads(content)
        except Exception as e:
            print(f"Error summarizing text: {str(e)}")
            return {
                "error": str(e),
                "summary": "Error generating summary.",
                "topics": [],
                "terms": [],
                "style": style
            }
    
    @staticmethod
    async def extract_text_from_url(url: str) -> str:
        """Extract main article text from a URL"""
        
        prompt = f"""
        Extract the main article text from this URL: {url}
        
        Only return the extracted content, nothing else.
        """
        
        try:
            response = text_model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            print(f"Error extracting text: {str(e)}")
            return f"Error: Could not extract text from URL. {str(e)}"
    
    @staticmethod
    async def chat_with_assistant(
        messages: List[Dict[str, str]], 
        context: Optional[str] = None
    ) -> str:
        """Chat with the AI assistant with memory of previous messages"""
        
        # Format messages for Gemini
        formatted_messages = []
        
        # Add context if provided
        if context:
            formatted_messages.append({
                "role": "system",
                "content": f"CONTEXT: {context}\n\nYou are a helpful language learning assistant for StudyWAI."
            })
        else:
            formatted_messages.append({
                "role": "system",
                "content": "You are a helpful language learning assistant for StudyWAI."
            })
        
        # Add user messages
        for msg in messages:
            formatted_messages.append(msg)
        
        try:
            # Format into prompt for Gemini
            prompt = "\n\n".join([f"{m['role'].upper()}: {m['content']}" for m in formatted_messages])
            response = text_model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"Error chatting with assistant: {str(e)}")
            return f"I'm sorry, I encountered an error: {str(e)}" 