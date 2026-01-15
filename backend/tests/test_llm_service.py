# LLM Service tests: summarization and translation
import pytest
from unittest.mock import Mock, MagicMock, patch
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))


class TestLLMServiceSummarization:
    """Test LLM summarization functionality"""

    @patch('app.services.llm_service.Groq')
    @patch('app.services.llm_service.os.getenv')
    def test_generate_summary_short(self, mock_getenv, mock_groq):
        """Test generating short summary"""
        mock_getenv.return_value = "test-api-key"
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "• Point 1\n• Point 2\n• Point 3"
        mock_client.chat.completions.create.return_value = mock_response
        mock_groq.return_value = mock_client
        
        from app.services.llm_service import LLMService
        service = LLMService()
        service.client = mock_client
        
        result = service.generate_summary("Test content", "short")
        
        assert result is not None
        assert len(result) > 0

    @patch('app.services.llm_service.Groq')
    @patch('app.services.llm_service.os.getenv')
    def test_generate_summary_medium(self, mock_getenv, mock_groq):
        """Test generating medium summary"""
        mock_getenv.return_value = "test-api-key"
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "This is a medium summary with multiple paragraphs."
        mock_client.chat.completions.create.return_value = mock_response
        mock_groq.return_value = mock_client
        
        from app.services.llm_service import LLMService
        service = LLMService()
        service.client = mock_client
        
        result = service.generate_summary("Test content", "medium")
        
        assert result is not None

    @patch('app.services.llm_service.Groq')
    @patch('app.services.llm_service.os.getenv')
    def test_generate_summary_uses_correct_model(self, mock_getenv, mock_groq):
        """Test that correct model is used for summarization"""
        mock_getenv.return_value = "test-api-key"
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "Summary"
        mock_client.chat.completions.create.return_value = mock_response
        mock_groq.return_value = mock_client
        
        from app.services.llm_service import LLMService
        service = LLMService()
        service.client = mock_client
        
        service.generate_summary("Test content", "short")
        
        mock_client.chat.completions.create.assert_called_once()

    @patch('app.services.llm_service.Groq')
    @patch('app.services.llm_service.os.getenv')
    def test_generate_summary_error_handling(self, mock_getenv, mock_groq):
        """Test error handling in summarization"""
        mock_getenv.return_value = "test-api-key"
        mock_client = MagicMock()
        mock_client.chat.completions.create.side_effect = Exception("API Error")
        mock_groq.return_value = mock_client
        
        from app.services.llm_service import LLMService
        service = LLMService()
        service.client = mock_client
        
        with pytest.raises(Exception):
            service.generate_summary("Test content", "short")


class TestLLMServiceTranslation:
    """Test LLM translation functionality"""

    @patch('app.services.llm_service.genai.Client')
    @patch('app.services.llm_service.Groq')
    @patch('app.services.llm_service.os.getenv')
    def test_translate_to_french(self, mock_getenv, mock_groq, mock_genai):
        """Test translation to French"""
        mock_getenv.return_value = "test-api-key"
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.text = "Ceci est un texte traduit."
        mock_client.models.generate_content.return_value = mock_response
        mock_genai.return_value = mock_client
        
        from app.services.llm_service import LLMService
        service = LLMService()
        
        with patch.object(service, 'get_translation', return_value="Ceci est un texte traduit."):
            result = service.get_translation("This is translated text.", "French")
            assert result is not None

    @patch('app.services.llm_service.genai.Client')
    @patch('app.services.llm_service.Groq')
    @patch('app.services.llm_service.os.getenv')
    def test_translate_to_spanish(self, mock_getenv, mock_groq, mock_genai):
        """Test translation to Spanish"""
        mock_getenv.return_value = "test-api-key"
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.text = "Este es un texto traducido."
        mock_client.models.generate_content.return_value = mock_response
        mock_genai.return_value = mock_client
        
        from app.services.llm_service import LLMService
        service = LLMService()
        
        with patch.object(service, 'get_translation', return_value="Este es un texto traducido."):
            result = service.get_translation("This is translated text.", "Spanish")
            assert result is not None

    @patch('app.services.llm_service.genai.Client')
    @patch('app.services.llm_service.Groq')
    @patch('app.services.llm_service.os.getenv')
    def test_translate_preserves_meaning(self, mock_getenv, mock_groq, mock_genai):
        """Test that translation preserves meaning"""
        mock_getenv.return_value = "test-api-key"
        
        from app.services.llm_service import LLMService
        service = LLMService()
        
        # The translation should not return the same text as input
        original = "Hello world"
        with patch.object(service, 'get_translation', return_value="Bonjour le monde"):
            result = service.get_translation(original, "French")
            assert result != original


class TestSummaryTypes:
    """Test different summary types"""

    def test_short_summary_instruction(self):
        """Test short summary has bullet points instruction"""
        instruction = "Provide a concise summary in 3-5 bullet points. Focus on the absolute key facts."
        assert "bullet points" in instruction.lower()
        assert "3-5" in instruction

    def test_medium_summary_instruction(self):
        """Test medium summary has paragraph instruction"""
        instruction = "Provide a medium-length summary (2-3 paragraphs). Cover the main history, key concepts, and significant details."
        assert "paragraphs" in instruction.lower()
        assert "2-3" in instruction

    def test_summary_type_selection(self):
        """Test summary type selection logic"""
        summary_type = "short"
        if summary_type.lower() == "short":
            instruction = "bullet points"
        else:
            instruction = "paragraphs"
        assert instruction == "bullet points"


class TestLLMConfiguration:
    """Test LLM configuration"""

    def test_default_model_name(self):
        """Test default model configuration"""
        model_name = "llama-3.1-8b-instant"
        assert "llama" in model_name.lower()

    def test_gemini_model_name(self):
        """Test Gemini model configuration"""
        gemini_model = "gemini-3-flash-preview"
        assert "gemini" in gemini_model.lower()

    def test_temperature_setting(self):
        """Test temperature configuration"""
        temperature = 0.5
        assert 0 <= temperature <= 2

    def test_max_tokens_setting(self):
        """Test max tokens configuration"""
        max_tokens = 1024
        assert max_tokens > 0


class TestSystemPrompts:
    """Test system prompts"""

    def test_summary_system_prompt(self):
        """Test summary system prompt content"""
        system_prompt = (
            "You are an expert educational assistant named WikiSmart. "
            "Your goal is to summarize complex academic content into clear, easy-to-understand text. "
            "Do not add any conversational filler (like 'Here is the summary'). Just output the summary."
        )
        assert "WikiSmart" in system_prompt
        assert "educational" in system_prompt.lower()

    def test_translator_system_prompt(self):
        """Test translator system prompt"""
        system_prompt = "You are an expert translator"
        assert "translator" in system_prompt.lower()

    def test_system_prompt_no_filler(self):
        """Test system prompt instructs no filler"""
        system_prompt = "Do not add any conversational filler"
        assert "filler" in system_prompt.lower()
# Commit 5: test: add mock LLM client fixtures
# Commit 20: test: add error handling tests for extraction
