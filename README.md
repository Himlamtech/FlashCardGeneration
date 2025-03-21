# Flash Card Generation using AI

A powerful flashcard application that leverages Google's Gemini AI to help you learn and memorize new words effectively.

![Flash Card Generation Preview](app/static/img/readme.txt)

## Features

- **AI-Powered Flashcards**: Create flashcards with Google's Gemini AI automatically generating translations, pronunciation, and example sentences
- **Flashcard Management**: Create, edit, and delete flashcards as needed
- **Interactive Study System**: User-friendly interface for studying your flashcards
- **CSV Storage**: All flashcards are stored in CSV format for easy access and portability
- **Additional AI Tools**: Grammar checking, text translation, and text summarization tools

## Setup

### Prerequisites

- Python 3.8 or higher
- A Google Gemini API key (get one at [Google AI Studio](https://makersuite.google.com/app/apikey))

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/flashcard-generation.git
   cd flashcard-generation
   ```

2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the project root with your Gemini API key:
   ```
   GEMINI_API_KEY=your_api_key_here
   ```

4. Run the application:
   ```
   python app.py
   ```

5. Open your browser and go to `http://127.0.0.1:5000`

## Usage

1. **Create Flashcards**: Click the "Create Flashcard" button, enter a word, and select the language. The AI will generate translations, pronunciation, and example sentences.

2. **Study Flashcards**: Navigate to the Study page to review your flashcards.

3. **Edit or Delete Flashcards**: Click the edit or delete buttons on any flashcard to modify or remove it.

4. **Use AI Tools**: Access the grammar check, translation, and summarization tools in the Study page.

## Technologies Used

- **Backend**: FastAPI
- **Frontend**: Bootstrap 5, jQuery
- **AI**: Google Generative AI (Gemini 2.0 Flash Lite)
- **Data Management**: Pandas
- **Deployment**: Uvicorn

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Inspired by Quizlet's flashcard system
- Powered by Google's Gemini AI 