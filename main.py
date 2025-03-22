import uvicorn

if __name__ == "__main__":
    """
    Run the StudyWAI application with Uvicorn server
    
    To start the application, run:
    python main.py
    
    For development with auto-reload:
    uvicorn app.app:app --reload
    """
    uvicorn.run("app.app:app", host="0.0.0.0", port=8000, reload=True) 