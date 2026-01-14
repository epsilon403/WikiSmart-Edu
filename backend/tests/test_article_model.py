# Article model tests
import pytest
from datetime import datetime
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app.models.article import Article, ActionType


class TestArticleModel:
    """Test Article model"""

    def test_article_creation(self, sample_article):
        """Test article instance creation"""
        assert sample_article.id == 1
        assert sample_article.user_id == 1
        assert "wikipedia" in sample_article.url
        assert sample_article.title == "Python (programming language)"

    def test_article_has_required_fields(self, sample_article):
        """Test that article has all required fields"""
        assert hasattr(sample_article, 'id')
        assert hasattr(sample_article, 'user_id')
        assert hasattr(sample_article, 'url')
        assert hasattr(sample_article, 'title')
        assert hasattr(sample_article, 'action')
        assert hasattr(sample_article, 'created_at')

    def test_article_action_is_enum(self, sample_article):
        """Test article action is ActionType enum"""
        assert sample_article.action in [ActionType.SUMMARY, ActionType.TRANSLATION, ActionType.QUIZ]


class TestActionType:
    """Test ActionType enum"""

    def test_action_type_summary(self):
        """Test SUMMARY action type"""
        assert ActionType.SUMMARY == "summary"

    def test_action_type_translation(self):
        """Test TRANSLATION action type"""
        assert ActionType.TRANSLATION == "translation"

    def test_action_type_quiz(self):
        """Test QUIZ action type"""
        assert ActionType.QUIZ == "quiz"

    def test_action_type_is_string_enum(self):
        """Test ActionType is string enum"""
        assert isinstance(ActionType.SUMMARY, str)
        assert isinstance(ActionType.TRANSLATION, str)
        assert isinstance(ActionType.QUIZ, str)

    def test_action_type_values(self):
        """Test all action type values"""
        expected_values = {"summary", "translation", "quiz"}
        actual_values = {at.value for at in ActionType}
        assert expected_values == actual_values


class TestArticleURL:
    """Test article URL handling"""

    def test_valid_wikipedia_url(self, sample_article):
        """Test valid Wikipedia URL"""
        assert "wikipedia.org" in sample_article.url

    def test_url_not_empty(self, sample_article):
        """Test URL is not empty"""
        assert len(sample_article.url) > 0

    def test_url_is_string(self, sample_article):
        """Test URL is string"""
        assert isinstance(sample_article.url, str)


class TestArticleTitle:
    """Test article title handling"""

    def test_title_not_empty(self, sample_article):
        """Test title is not empty"""
        assert len(sample_article.title) > 0

    def test_title_is_string(self, sample_article):
        """Test title is string"""
        assert isinstance(sample_article.title, str)

    def test_title_readable(self, sample_article):
        """Test title is readable (no underscores)"""
        assert "_" not in sample_article.title or " " in sample_article.title


class TestArticleTimestamp:
    """Test article timestamp"""

    def test_created_at_is_datetime(self, sample_article):
        """Test created_at is datetime"""
        assert isinstance(sample_article.created_at, datetime)

    def test_created_at_not_future(self, sample_article):
        """Test created_at is not in future"""
        assert sample_article.created_at <= datetime.utcnow()


class TestArticleRelationships:
    """Test article relationships"""

    def test_article_has_user_relationship(self):
        """Test article has user relationship defined"""
        assert hasattr(Article, 'user')

    def test_article_has_quiz_attempts_relationship(self):
        """Test article has quiz_attempts relationship defined"""
        assert hasattr(Article, 'quiz_attempts')


class TestArticleCreation:
    """Test article creation scenarios"""

    def test_create_summary_article(self):
        """Test creating article with summary action"""
        article = Article(
            id=1,
            user_id=1,
            url="https://en.wikipedia.org/wiki/Test",
            title="Test",
            action=ActionType.SUMMARY,
            created_at=datetime.utcnow()
        )
        assert article.action == ActionType.SUMMARY

    def test_create_translation_article(self):
        """Test creating article with translation action"""
        article = Article(
            id=2,
            user_id=1,
            url="https://en.wikipedia.org/wiki/Test",
            title="Test",
            action=ActionType.TRANSLATION,
            created_at=datetime.utcnow()
        )
        assert article.action == ActionType.TRANSLATION

    def test_create_quiz_article(self):
        """Test creating article with quiz action"""
        article = Article(
            id=3,
            user_id=1,
            url="https://en.wikipedia.org/wiki/Test",
            title="Test",
            action=ActionType.QUIZ,
            created_at=datetime.utcnow()
        )
        assert article.action == ActionType.QUIZ
# Commit 12: test: add user authentication tests
