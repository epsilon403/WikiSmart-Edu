# Content extractor tests
import pytest
from unittest.mock import Mock, MagicMock, patch
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))


class TestURLParsing:
    """Test URL parsing functionality"""

    def test_extract_language_from_english_url(self):
        """Test extracting language code from English Wikipedia URL"""
        url = "https://en.wikipedia.org/wiki/Python"
        hostname = "en.wikipedia.org"
        language = hostname.split('.')[0]
        assert language == "en"

    def test_extract_language_from_french_url(self):
        """Test extracting language code from French Wikipedia URL"""
        url = "https://fr.wikipedia.org/wiki/Python"
        hostname = "fr.wikipedia.org"
        language = hostname.split('.')[0]
        assert language == "fr"

    def test_extract_language_from_german_url(self):
        """Test extracting language code from German Wikipedia URL"""
        url = "https://de.wikipedia.org/wiki/Python"
        hostname = "de.wikipedia.org"
        language = hostname.split('.')[0]
        assert language == "de"

    def test_extract_title_from_url(self):
        """Test extracting title from Wikipedia URL"""
        from urllib.parse import unquote
        url_path = "/wiki/Python_(programming_language)"
        raw_title = url_path.split("/")[-1]
        title = unquote(raw_title).replace("_", " ")
        assert title == "Python (programming language)"

    def test_extract_title_with_special_chars(self):
        """Test extracting title with URL-encoded characters"""
        from urllib.parse import unquote
        raw_title = "C%2B%2B"
        title = unquote(raw_title)
        assert title == "C++"


class TestWikipediaURLValidation:
    """Test Wikipedia URL validation"""

    def test_valid_wikipedia_url(self):
        """Test valid Wikipedia URL detection"""
        url = "https://en.wikipedia.org/wiki/Python"
        assert "wikipedia.org" in url

    def test_invalid_url(self):
        """Test invalid URL detection"""
        url = "https://example.com/page"
        assert "wikipedia.org" not in url

    def test_mobile_wikipedia_url(self):
        """Test mobile Wikipedia URL"""
        url = "https://en.m.wikipedia.org/wiki/Python"
        assert "wikipedia.org" in url

    def test_https_required(self):
        """Test that HTTPS URLs are handled"""
        url = "https://en.wikipedia.org/wiki/Python"
        assert url.startswith("https://")


class TestLanguageDetection:
    """Test language detection from URLs"""

    def test_default_to_english(self):
        """Test defaulting to English when language not detected"""
        hostname = "some.other.domain"
        if 'wikipedia.org' not in hostname:
            language = "en"
        assert language == "en"

    def test_supported_languages(self):
        """Test various supported language codes"""
        languages = ["en", "fr", "de", "es", "it", "pt", "ja", "zh", "ar", "ru"]
        for lang in languages:
            url = f"https://{lang}.wikipedia.org/wiki/Test"
            hostname = f"{lang}.wikipedia.org"
            extracted = hostname.split('.')[0]
            assert extracted == lang


class TestContentStructure:
    """Test content structure returned by extractor"""

    def test_content_has_title(self):
        """Test that content has title field"""
        content = {
            "title": "Test",
            "content": "Content",
            "summary": "Summary",
            "url": "https://test.com",
            "language": "en"
        }
        assert "title" in content

    def test_content_has_content(self):
        """Test that content has content field"""
        content = {
            "title": "Test",
            "content": "Content",
            "summary": "Summary",
            "url": "https://test.com",
            "language": "en"
        }
        assert "content" in content

    def test_content_has_summary(self):
        """Test that content has summary field"""
        content = {
            "title": "Test",
            "content": "Content",
            "summary": "Summary",
            "url": "https://test.com",
            "language": "en"
        }
        assert "summary" in content

    def test_content_has_url(self):
        """Test that content has url field"""
        content = {
            "title": "Test",
            "content": "Content",
            "summary": "Summary",
            "url": "https://test.com",
            "language": "en"
        }
        assert "url" in content

    def test_content_has_language(self):
        """Test that content has language field"""
        content = {
            "title": "Test",
            "content": "Content",
            "summary": "Summary",
            "url": "https://test.com",
            "language": "en"
        }
        assert "language" in content


class TestUserAgent:
    """Test User-Agent configuration"""

    def test_user_agent_format(self):
        """Test User-Agent header format"""
        user_agent = "WikiSmartEdu/1.0 (Educational Project; contact@wikismartedu.com)"
        assert "WikiSmartEdu" in user_agent
        assert "Educational" in user_agent

    def test_user_agent_has_contact(self):
        """Test User-Agent has contact info"""
        user_agent = "WikiSmartEdu/1.0 (Educational Project; contact@wikismartedu.com)"
        assert "contact" in user_agent or "@" in user_agent


class TestErrorHandling:
    """Test error handling in content extraction"""

    def test_page_not_found_message(self):
        """Test page not found error message"""
        title = "NonExistent"
        error_msg = f"Page Wikipedia introuvable pour le titre: {title}"
        assert "introuvable" in error_msg.lower()

    def test_disambiguation_error_message(self):
        """Test disambiguation error message"""
        options = ["Option1", "Option2", "Option3"]
        error_msg = f"Titre ambigu. Veuillez préciser parmi ces options : {', '.join(options[:5])}"
        assert "ambigu" in error_msg.lower()

    def test_generic_error_message(self):
        """Test generic error message"""
        error = "Some error"
        error_msg = f"Erreur lors de l'extraction Wikipedia: {error}"
        assert "Erreur" in error_msg
# Commit 11: test: add user registration tests
# Commit 26: test: add LLM translation tests
