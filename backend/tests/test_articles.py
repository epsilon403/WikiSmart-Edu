# Article tests: content extraction, preprocessing, summarization
import pytest
from unittest.mock import Mock, MagicMock, patch, AsyncMock
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app.services.content_extractor import get_wikipedia_content
from app.services.preprocessor import clean_and_segment_text, clean_text, split_into_chunks


class TestWikipediaContentExtraction:
    """Test Wikipedia content extraction"""

    @patch('app.services.content_extractor.wikipedia')
    @patch('app.services.content_extractor.requests.Session')
    def test_extract_english_wikipedia(self, mock_session, mock_wikipedia):
        """Test extracting content from English Wikipedia"""
        mock_page = MagicMock()
        mock_page.title = "Python (programming language)"
        mock_page.content = "Python is a programming language."
        mock_page.summary = "Python is a high-level language."
        mock_page.url = "https://en.wikipedia.org/wiki/Python"
        mock_wikipedia.page.return_value = mock_page
        
        result = get_wikipedia_content("https://en.wikipedia.org/wiki/Python_(programming_language)")
        
        assert result["title"] == "Python (programming language)"
        assert "Python" in result["content"]

    @patch('app.services.content_extractor.wikipedia')
    @patch('app.services.content_extractor.requests.Session')
    def test_extract_french_wikipedia(self, mock_session, mock_wikipedia):
        """Test extracting content from French Wikipedia"""
        mock_page = MagicMock()
        mock_page.title = "Python (langage)"
        mock_page.content = "Python est un langage de programmation."
        mock_page.summary = "Python est un langage."
        mock_page.url = "https://fr.wikipedia.org/wiki/Python"
        mock_wikipedia.page.return_value = mock_page
        
        result = get_wikipedia_content("https://fr.wikipedia.org/wiki/Python_(langage)")
        
        assert result["language"] == "fr"

    @patch('app.services.content_extractor.wikipedia')
    @patch('app.services.content_extractor.requests.Session')
    def test_extract_with_explicit_language(self, mock_session, mock_wikipedia):
        """Test extraction with explicit language parameter"""
        mock_page = MagicMock()
        mock_page.title = "Test"
        mock_page.content = "Test content"
        mock_page.summary = "Test summary"
        mock_page.url = "https://de.wikipedia.org/wiki/Test"
        mock_wikipedia.page.return_value = mock_page
        
        result = get_wikipedia_content("https://de.wikipedia.org/wiki/Test", language="de")
        
        mock_wikipedia.set_lang.assert_called_with("de")

    @patch('app.services.content_extractor.wikipedia')
    @patch('app.services.content_extractor.requests.Session')
    def test_extract_page_not_found(self, mock_session, mock_wikipedia):
        """Test handling of page not found error"""
        import wikipedia as wiki_module
        mock_wikipedia.page.side_effect = wiki_module.exceptions.PageError("NonExistent")
        mock_wikipedia.exceptions = wiki_module.exceptions
        
        with pytest.raises(Exception) as exc_info:
            get_wikipedia_content("https://en.wikipedia.org/wiki/NonExistent_Page_12345")
        
        assert "introuvable" in str(exc_info.value).lower() or "not found" in str(exc_info.value).lower()

    @patch('app.services.content_extractor.wikipedia')
    @patch('app.services.content_extractor.requests.Session')
    def test_extract_url_with_special_characters(self, mock_session, mock_wikipedia):
        """Test extraction from URL with special characters"""
        mock_page = MagicMock()
        mock_page.title = "C++"
        mock_page.content = "C++ is a programming language."
        mock_page.summary = "C++ is a language."
        mock_page.url = "https://en.wikipedia.org/wiki/C%2B%2B"
        mock_wikipedia.page.return_value = mock_page
        
        result = get_wikipedia_content("https://en.wikipedia.org/wiki/C%2B%2B")
        
        assert result is not None


class TestTextCleaning:
    """Test text cleaning functionality"""

    def test_clean_text_removes_multiple_spaces(self):
        """Test that multiple spaces are reduced to single space"""
        text = "Hello    world   test"
        result = clean_text(text)
        assert "    " not in result
        assert "Hello world test" == result

    def test_clean_text_removes_multiple_newlines(self):
        """Test that multiple newlines are reduced"""
        text = "Hello\n\n\n\nworld"
        result = clean_text(text)
        assert "\n\n" not in result

    def test_clean_text_strips_whitespace(self):
        """Test that leading/trailing whitespace is removed"""
        text = "   Hello world   "
        result = clean_text(text)
        assert result == "Hello world"

    def test_clean_text_empty_string(self):
        """Test cleaning empty string"""
        result = clean_text("")
        assert result == ""

    def test_clean_text_preserves_content(self):
        """Test that actual content is preserved"""
        text = "Python is great"
        result = clean_text(text)
        assert "Python" in result
        assert "great" in result


class TestTextSegmentation:
    """Test text segmentation functionality"""

    def test_segment_text_creates_sections(self, sample_raw_text):
        """Test that text is segmented into sections"""
        result = clean_and_segment_text(sample_raw_text)
        assert isinstance(result, dict)
        assert len(result) > 0

    def test_segment_text_has_introduction(self):
        """Test that Introduction section is created"""
        text = "This is the introduction.\n\nSection One\nThis is section one content."
        result = clean_and_segment_text(text)
        assert "Introduction" in result or "Content" in result

    def test_segment_text_detects_sections(self):
        """Test that section headers are detected"""
        text = """Introduction to Python

        Python is a language.

        History
        
        Python was created in 1991.
        
        Features
        
        Python is dynamically typed."""
        result = clean_and_segment_text(text)
        assert len(result) >= 1

    def test_segment_text_empty_input(self):
        """Test segmentation of empty string"""
        result = clean_and_segment_text("")
        assert isinstance(result, dict)

    def test_segment_text_single_paragraph(self):
        """Test segmentation of single paragraph"""
        text = "This is just a single paragraph with no sections."
        result = clean_and_segment_text(text)
        assert len(result) >= 1


class TestTextChunking:
    """Test text chunking functionality"""

    def test_split_into_chunks_short_text(self):
        """Test that short text returns single chunk"""
        text = "Short text"
        chunks = split_into_chunks(text, chunk_size=1000)
        assert len(chunks) == 1
        assert chunks[0] == "Short text"

    def test_split_into_chunks_long_text(self):
        """Test that long text is split into multiple chunks"""
        text = "a" * 5000
        chunks = split_into_chunks(text, chunk_size=1000, overlap=200)
        assert len(chunks) > 1

    def test_split_into_chunks_overlap(self):
        """Test that chunks have overlap"""
        text = "a" * 3000
        chunks = split_into_chunks(text, chunk_size=1000, overlap=200)
        # With overlap, chunks should share some content
        assert len(chunks) >= 3

    def test_split_into_chunks_respects_sentences(self):
        """Test that chunking tries to respect sentence boundaries"""
        text = "First sentence. Second sentence. " * 100
        chunks = split_into_chunks(text, chunk_size=100, overlap=20)
        # Chunks should generally end at periods
        for chunk in chunks[:-1]:
            assert chunk.endswith('.') or len(chunk) >= 100

    def test_split_into_chunks_custom_sizes(self):
        """Test chunking with custom sizes"""
        text = "word " * 500
        chunks = split_into_chunks(text, chunk_size=500, overlap=100)
        for chunk in chunks:
            assert len(chunk) <= 550  # Allow some flexibility for word boundaries


class TestArticleModel:
    """Test Article model"""

    def test_article_creation(self, sample_article):
        """Test article instance creation"""
        assert sample_article.id == 1
        assert sample_article.user_id == 1
        assert "wikipedia" in sample_article.url

    def test_article_action_types(self):
        """Test different action types"""
        from app.models.article import ActionType
        assert ActionType.SUMMARY == "summary"
        assert ActionType.TRANSLATION == "translation"
        assert ActionType.QUIZ == "quiz"

    def test_article_has_required_fields(self, sample_article):
        """Test that article has all required fields"""
        assert hasattr(sample_article, 'id')
        assert hasattr(sample_article, 'user_id')
        assert hasattr(sample_article, 'url')
        assert hasattr(sample_article, 'title')
        assert hasattr(sample_article, 'action')
        assert hasattr(sample_article, 'created_at')
# Commit 3: test: add sample user and admin fixtures
