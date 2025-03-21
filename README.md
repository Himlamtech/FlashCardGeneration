# Flash Card Generation using AI

A flashcard application that uses Google's Gemini AI to automatically generate comprehensive flashcards for language learning.

![Flashcard AI](app/static/img/preview.png)

## Features

- **AI-Powered Flashcards**: Generate flashcards from English or Vietnamese words with translations, pronunciation, and example sentences using Gemini AI
- **Flashcard Management**: Add, edit, and delete flashcards
- **Study System**: Interactive study mode with spaced repetition learning
- **CSV Storage**: Simple and portable database format
- **Additional AI Tools**:
  - Grammar checking
  - Text translation
  - Text summarization

## Setup Instructions

### Prerequisites

- Python 3.8+
- Google Gemini API key

### Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd FlashCardGeneration
   ```

2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the project root with the following content:
   ```
   GEMINI_API_KEY=your_gemini_api_key_here
   FLASK_SECRET_KEY=generate_a_random_secret_key_here
   ```

4. Run the application:
   ```bash
   python app.py
   ```

5. Open your browser and navigate to:
   ```
   http://127.0.0.1:5000/
   ```

## Usage

### Creating Flashcards

1. Click on "Create Flashcard" in the navigation bar
2. Enter a word and select its language
3. Click "Generate Flashcard with AI"
4. The AI will automatically generate translations, pronunciation, and example sentences

### Studying Flashcards

1. Click on "Study" in the navigation bar
2. Study your flashcards using the interactive study mode
3. Mark cards as correct or incorrect to track your progress
4. Use study settings to customize your learning experience

### Additional AI Tools

- **Grammar Check**: Check your text for grammar errors using AI
- **AI Translation**: Translate text between languages with AI
- **Text Summarization**: Generate concise summaries of longer texts

## Technologies Used

- Flask (Python web framework)
- Bootstrap 5 (Frontend styling)
- Google Generative AI (Gemini API)
- Pandas (Data handling)
- jQuery (Frontend interactivity)

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- Inspired by Quizlet's flashcard learning system
- Powered by Google's Gemini AI
- Built with Flask framework 