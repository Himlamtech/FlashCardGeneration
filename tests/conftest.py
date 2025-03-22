import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.app import app
from database.database import Base, get_db
from models.models import Flashcard

# Create in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def test_db():
    # Create the tables
    Base.metadata.create_all(bind=engine)
    
    # Use our test database instead of the real one
    def override_get_db():
        try:
            db = TestingSessionLocal()
            yield db
        finally:
            db.close()
    
    app.dependency_overrides[get_db] = override_get_db
    
    # Add some test data
    db = TestingSessionLocal()
    sample_flashcard = Flashcard(
        id="test-id-1",
        word="hello",
        language="english",
        translations="hola, bonjour",
        pronunciation="hə-ˈlō",
        examples="Hello, how are you?|Hello world!|She said hello to me."
    )
    db.add(sample_flashcard)
    db.commit()
    
    yield  # Run the tests
    
    # Cleanup - drop all tables
    Base.metadata.drop_all(bind=engine)
    app.dependency_overrides.clear()

@pytest.fixture
def client(test_db):
    with TestClient(app) as c:
        yield c 