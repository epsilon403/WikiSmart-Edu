# Configuration tests
import pytest
from unittest.mock import patch
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))


class TestSettings:
    """Test Settings configuration"""

    def test_project_name(self):
        """Test project name setting"""
        from app.core.config import settings
        assert settings.PROJECT_NAME == "WikiSmart-Edu"

    def test_version(self):
        """Test version setting"""
        from app.core.config import settings
        assert settings.VERSION == "1.0.0"

    def test_algorithm(self):
        """Test JWT algorithm setting"""
        from app.core.config import settings
        assert settings.ALGORITHM == "HS256"

    def test_access_token_expire(self):
        """Test access token expiration setting"""
        from app.core.config import settings
        assert settings.ACCESS_TOKEN_EXPIRE_MINUTES == 30

    def test_allowed_origins(self):
        """Test CORS allowed origins"""
        from app.core.config import settings
        assert isinstance(settings.ALLOWED_ORIGINS, list)
        assert len(settings.ALLOWED_ORIGINS) > 0


class TestDatabaseConfig:
    """Test database configuration"""

    def test_database_url_format(self):
        """Test database URL format"""
        from app.core.config import settings
        assert "postgresql" in settings.DATABASE_URL or "sqlite" in settings.DATABASE_URL


class TestSecurityConfig:
    """Test security configuration"""

    def test_secret_key_exists(self):
        """Test secret key is configured"""
        from app.core.config import settings
        assert settings.SECRET_KEY is not None
        assert len(settings.SECRET_KEY) > 0

    def test_refresh_secret_key_exists(self):
        """Test refresh secret key is configured"""
        from app.core.config import settings
        assert settings.REFRESH_SECRET_KEY is not None


class TestCORSConfig:
    """Test CORS configuration"""

    def test_localhost_allowed(self):
        """Test localhost is in allowed origins"""
        from app.core.config import settings
        localhost_origins = [o for o in settings.ALLOWED_ORIGINS if "localhost" in o]
        assert len(localhost_origins) > 0

    def test_multiple_ports_allowed(self):
        """Test multiple ports are allowed"""
        from app.core.config import settings
        ports = ["3000", "8501", "8001", "5173", "8000"]
        found_ports = 0
        for port in ports:
            for origin in settings.ALLOWED_ORIGINS:
                if port in origin:
                    found_ports += 1
                    break
        assert found_ports >= 3


class TestAPIKeysConfig:
    """Test API keys configuration"""

    def test_gemini_api_key_setting(self):
        """Test Gemini API key setting exists"""
        from app.core.config import settings
        assert hasattr(settings, 'GEMINI_API_KEY')

    def test_google_api_key_setting(self):
        """Test Google API key setting exists"""
        from app.core.config import settings
        assert hasattr(settings, 'GOOGLE_API_KEY')

    def test_groq_api_key_setting(self):
        """Test Groq API key setting exists"""
        from app.core.config import settings
        assert hasattr(settings, 'GROQ_API_KEY')


class TestConfigDefaults:
    """Test configuration defaults"""

    def test_debug_default(self):
        """Test debug default is False"""
        from app.core.config import settings
        assert settings.DEBUG is False

    def test_token_expire_default(self):
        """Test token expire has sensible default"""
        from app.core.config import settings
        assert settings.ACCESS_TOKEN_EXPIRE_MINUTES > 0
        assert settings.ACCESS_TOKEN_EXPIRE_MINUTES <= 60
# Commit 10: test: add token verification tests
# Commit 25: test: add LLM summarization tests
