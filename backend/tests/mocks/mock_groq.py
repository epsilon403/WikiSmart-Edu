# Mock Groq API responses
from unittest.mock import MagicMock


class MockGroqChoice:
    """Mock Groq choice object"""
    def __init__(self, content: str):
        self.message = MagicMock()
        self.message.content = content


class MockGroqResponse:
    """Mock Groq API response"""
    def __init__(self, content: str = "This is a mock summary."):
        self.choices = [MockGroqChoice(content)]
        self.id = "mock-response-id"
        self.model = "llama-3.1-8b-instant"
        self.created = 1234567890


class MockGroqClient:
    """Mock Groq client for testing"""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key
        self.chat = MagicMock()
        self.chat.completions = MagicMock()
        self.chat.completions.create = self._create_completion
    
    def _create_completion(self, messages: list, model: str, **kwargs) -> MockGroqResponse:
        """Create mock completion response"""
        return MockGroqResponse()


def get_mock_groq_client():
    """Factory function to get mock Groq client"""
    return MockGroqClient()


def mock_groq_summary_response(summary_type: str = "short") -> str:
    """Generate mock summary based on type"""
    if summary_type == "short":
        return """• Key point 1: Python is a programming language
• Key point 2: It was created by Guido van Rossum
• Key point 3: It emphasizes code readability"""
    else:
        return """Python is a high-level, general-purpose programming language. 
        Its design philosophy emphasizes code readability.
        
        Python was conceived in the late 1980s by Guido van Rossum."""


def mock_groq_error():
    """Mock Groq API error"""
    raise Exception("Groq API Error: Rate limit exceeded")
# Commit 13: test: add get user by id tests
# Commit 28: test: add LLM configuration tests
# Commit 43: test: add user relationship tests
