# Pytest configuration and fixtures
import pytest
from unittest.mock import Mock, MagicMock, patch
from datetime import datetime, timedelta, timezone
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app.models.user import User, UserRole
from app.models.article import Article, ActionType
from app.models.quiz_attempt import QuizAttempt


@pytest.fixture
def mock_db_session():
    """Create a mock database session"""
    session = MagicMock()
    session.query.return_value.filter.return_value.first.return_value = None
    session.add = MagicMock()
    session.commit = MagicMock()
    session.refresh = MagicMock()
    return session


@pytest.fixture
def sample_user():
    """Create a sample user for testing"""
    user = User(
        id=1,
        username="testuser",
        email="test@example.com",
        hashed_password="$2b$12$hashedpassword",
        role=UserRole.USER,
        created_at=datetime.utcnow()
    )
    return user


@pytest.fixture
def sample_admin_user():
    """Create a sample admin user for testing"""
    user = User(
        id=2,
        username="admin",
        email="admin@example.com",
        hashed_password="$2b$12$hashedpassword",
        role=UserRole.ADMIN,
        created_at=datetime.utcnow()
    )
    return user


@pytest.fixture
def sample_article():
    """Create a sample article for testing"""
    article = Article(
        id=1,
        user_id=1,
        url="https://en.wikipedia.org/wiki/Python_(programming_language)",
        title="Python (programming language)",
        action=ActionType.SUMMARY,
        created_at=datetime.utcnow()
    )
    return article


@pytest.fixture
def sample_quiz_attempt():
    """Create a sample quiz attempt for testing"""
    attempt = QuizAttempt(
        id=1,
        user_id=1,
        article_id=1,
        score=85.0,
        submitted_at=datetime.utcnow()
    )
    return attempt


@pytest.fixture
def sample_wikipedia_content():
    """Sample Wikipedia content for testing"""
    return {
        "title": "Python (programming language)",
        "content": """Python is a high-level, general-purpose programming language. 
        Its design philosophy emphasizes code readability with the use of significant indentation.
        
        History
        Python was conceived in the late 1980s by Guido van Rossum at Centrum Wiskunde & Informatica.
        
        Features
        Python is dynamically typed and garbage-collected. It supports multiple programming paradigms.""",
        "summary": "Python is a high-level programming language.",
        "url": "https://en.wikipedia.org/wiki/Python_(programming_language)",
        "language": "en"
    }


@pytest.fixture
def sample_raw_text():
    """Sample raw text for preprocessing tests"""
    return """Python Programming Language

    Python is a high-level programming language.    It was created by Guido van Rossum.
    
    
    History
    
    Python was first released in 1991.
    
    Features
    
    Python supports multiple programming paradigms.
    It is dynamically typed and garbage collected."""


@pytest.fixture
def mock_groq_client():
    """Mock Groq client for testing"""
    mock_client = MagicMock()
    mock_response = MagicMock()
    mock_response.choices = [MagicMock()]
    mock_response.choices[0].message.content = "This is a test summary."
    mock_client.chat.completions.create.return_value = mock_response
    return mock_client


@pytest.fixture
def mock_gemini_client():
    """Mock Gemini client for testing"""
    mock_client = MagicMock()
    mock_response = MagicMock()
    mock_response.text = "Ceci est une traduction de test."
    mock_client.models.generate_content.return_value = mock_response
    return mock_client


@pytest.fixture
def valid_jwt_payload():
    """Valid JWT payload for testing"""
    return {
        "sub": "testuser",
        "user_id": 1,
        "exp": datetime.now(timezone.utc) + timedelta(minutes=30)
    }


@pytest.fixture
def expired_jwt_payload():
    """Expired JWT payload for testing"""
    return {
        "sub": "testuser",
        "user_id": 1,
        "exp": datetime.now(timezone.utc) - timedelta(minutes=30)
    }
# Commit 1: test: initialize pytest configuration and fixtures
