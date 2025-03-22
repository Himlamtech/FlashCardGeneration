# StudyWAI - AI-Powered Flashcard Application

StudyWAI is a modern, AI-powered flashcard application designed to help language learners create, study, and master vocabulary with the assistance of generative AI.

## Features

- **AI-Generated Flashcards**: Automatically generate comprehensive flashcards with translations, pronunciation guides, and example sentences
- **Interactive Study Mode**: Review flashcards with a spaced repetition system to optimize learning
- **Translation Tool**: Translate text between multiple languages and create flashcards directly from translations
- **Grammar Checking**: Check your writing for grammar, spelling, style, and punctuation issues
- **Text Summarization**: Summarize long texts and extract key terms for flashcard creation
- **AI Assistant**: Chat with an AI tutor to get help with language learning questions
- **Modern UI**: Clean and responsive design that works on desktop and mobile devices

## Technology Stack
image.png
- **Backend**: FastAPI (Python)
- **Frontend**: HTML, CSS, JavaScript, Bootstrap 5, jQuery
- **Database**: SQLite (via SQLAlchemy)
- **AI**: Google Gemini AI

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/studywai.git
cd studywai
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the root directory with your Google Gemini API key:
```
GOOGLE_AI_API_KEY=your_api_key_here
```

5. Run the application:
```bash
uvicorn app.app:app --reload
```

6. Open your browser and navigate to http://localhost:8000

## Project Structure

```
studywai/
├── app/
│   ├── static/
│   │   ├── css/
│   │   ├── js/
│   │   └── img/
│   └── templates/
├── ai/
├── database/
├── models/
├── utils/
├── app.py
├── .env
└── requirements.txt
```

## API Endpoints

The application exposes the following API endpoints:

- `/api/translate` - Translate text between languages
- `/api/grammar-check` - Check text for grammar issues
- `/api/summarize` - Summarize long text
- `/api/extract-url` - Extract text from a URL
- `/api/chat` - Chat with the AI assistant

## Development

To contribute to this project:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/your-feature`)
3. Make your changes
4. Run tests (`pytest`)
5. Commit your changes (`git commit -m 'Add some feature'`)
6. Push to the branch (`git push origin feature/your-feature`)
7. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- Google Gemini AI for powering the generative AI features
- FastAPI for the backend framework
- Bootstrap for the frontend components 