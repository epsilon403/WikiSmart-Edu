# Mock Gemini API responses
from unittest.mock import MagicMock


class MockGeminiResponse:
    """Mock Gemini API response"""
    def __init__(self, text: str = "Ceci est une traduction mock."):
        self.text = text
        self.candidates = [MagicMock()]
        self.candidates[0].content = MagicMock()
        self.candidates[0].content.parts = [MagicMock()]
        self.candidates[0].content.parts[0].text = text


class MockGeminiClient:
    """Mock Gemini client for testing"""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key
        self.models = MagicMock()
        self.models.generate_content = self._generate_content
    
    def _generate_content(self, model: str, contents: str, **kwargs) -> MockGeminiResponse:
        """Generate mock content response"""
        return MockGeminiResponse()


def get_mock_gemini_client():
    """Factory function to get mock Gemini client"""
    return MockGeminiClient()


def mock_translation_response(target_language: str) -> str:
    """Generate mock translation based on target language"""
    translations = {
        "French": "Ceci est une traduction en français.",
        "Spanish": "Esta es una traducción al español.",
        "German": "Dies ist eine Übersetzung ins Deutsche.",
        "Italian": "Questa è una traduzione in italiano.",
        "Portuguese": "Esta é uma tradução para o português.",
        "Arabic": "هذه ترجمة إلى العربية.",
        "Chinese": "这是中文翻译。",
        "Japanese": "これは日本語の翻訳です。"
    }
    return translations.get(target_language, f"Translation to {target_language}")


def mock_quiz_response(num_questions: int = 5) -> dict:
    """Generate mock quiz response"""
    questions = []
    for i in range(num_questions):
        questions.append({
            "question": f"Sample question {i+1} about the article?",
            "options": [
                f"Option A for question {i+1}",
                f"Option B for question {i+1}",
                f"Option C for question {i+1}",
                f"Option D for question {i+1}"
            ],
            "correct_answer": f"Option A for question {i+1}",
            "explanation": f"Explanation for question {i+1}"
        })
    return {"questions": questions}


def mock_gemini_error():
    """Mock Gemini API error"""
    raise Exception("Gemini API Error: Quota exceeded")
# Commit 14: test: add get user by username tests
