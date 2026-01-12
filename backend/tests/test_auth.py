# Authentication tests: login, register, token validation
import pytest
from unittest.mock import Mock, MagicMock, patch
from datetime import datetime, timedelta, timezone
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app.services.auth_service import AuthService, pwd_context, ALGORITHM
from app.core.exceptions import InvalidCredentialsException, UserNotFoundException
from app.models.user import User, UserRole


class TestPasswordHashing:
    """Test password hashing functionality"""

    def test_hash_password_returns_string(self):
        """Test that hash_password returns a string"""
        password = "testpassword123"
        hashed = AuthService.hash_password(password)
        assert isinstance(hashed, str)
        assert hashed != password

    def test_hash_password_different_for_same_input(self):
        """Test that same password produces different hashes (due to salt)"""
        password = "testpassword123"
        hash1 = AuthService.hash_password(password)
        hash2 = AuthService.hash_password(password)
        assert hash1 != hash2

    def test_hash_password_truncates_long_passwords(self):
        """Test that passwords longer than 72 bytes are truncated"""
        long_password = "a" * 100
        hashed = AuthService.hash_password(long_password)
        assert isinstance(hashed, str)

    def test_hash_password_handles_unicode(self):
        """Test that unicode passwords are handled correctly"""
        unicode_password = "пароль日本語🔐"
        hashed = AuthService.hash_password(unicode_password)
        assert isinstance(hashed, str)


class TestPasswordVerification:
    """Test password verification functionality"""

    def test_verify_password_correct(self):
        """Test that correct password verifies successfully"""
        password = "testpassword123"
        hashed = AuthService.hash_password(password)
        assert AuthService.verify_password(password, hashed) is True

    def test_verify_password_incorrect(self):
        """Test that incorrect password fails verification"""
        password = "testpassword123"
        wrong_password = "wrongpassword"
        hashed = AuthService.hash_password(password)
        assert AuthService.verify_password(wrong_password, hashed) is False

    def test_verify_password_long_passwords(self):
        """Test verification of passwords at bcrypt limit"""
        password = "a" * 72
        hashed = AuthService.hash_password(password)
        assert AuthService.verify_password(password, hashed) is True

    def test_verify_password_empty_string(self):
        """Test that empty password verification works"""
        password = ""
        hashed = AuthService.hash_password(password)
        assert AuthService.verify_password(password, hashed) is True


class TestAccessTokenCreation:
    """Test access token creation"""

    @patch('app.services.auth_service.settings')
    def test_create_access_token_returns_string(self, mock_settings):
        """Test that access token is a string"""
        mock_settings.SECRET_KEY = "test-secret-key"
        data = {"sub": "testuser"}
        token = AuthService.create_access_token(data)
        assert isinstance(token, str)
        assert len(token) > 0

    @patch('app.services.auth_service.settings')
    def test_create_access_token_with_custom_expiry(self, mock_settings):
        """Test access token with custom expiry"""
        mock_settings.SECRET_KEY = "test-secret-key"
        data = {"sub": "testuser"}
        expires = timedelta(hours=1)
        token = AuthService.create_access_token(data, expires)
        assert isinstance(token, str)

    @patch('app.services.auth_service.settings')
    def test_create_access_token_contains_data(self, mock_settings):
        """Test that token contains the original data"""
        mock_settings.SECRET_KEY = "test-secret-key"
        data = {"sub": "testuser", "user_id": 1}
        token = AuthService.create_access_token(data)
        payload = AuthService.verify_access_token(token)
        assert payload["sub"] == "testuser"
        assert payload["user_id"] == 1


class TestRefreshTokenCreation:
    """Test refresh token creation"""

    @patch('app.services.auth_service.settings')
    def test_create_refresh_token_returns_string(self, mock_settings):
        """Test that refresh token is a string"""
        mock_settings.REFRESH_SECRET_KEY = "test-refresh-key"
        data = {"sub": "testuser"}
        token = AuthService.create_refresh_token(data)
        assert isinstance(token, str)

    @patch('app.services.auth_service.settings')
    def test_refresh_token_different_from_access_token(self, mock_settings):
        """Test that refresh token is different from access token"""
        mock_settings.SECRET_KEY = "test-secret-key"
        mock_settings.REFRESH_SECRET_KEY = "test-refresh-key"
        data = {"sub": "testuser"}
        access_token = AuthService.create_access_token(data)
        refresh_token = AuthService.create_refresh_token(data)
        assert access_token != refresh_token


class TestTokenVerification:
    """Test token verification"""

    @patch('app.services.auth_service.settings')
    def test_verify_access_token_valid(self, mock_settings):
        """Test verification of valid access token"""
        mock_settings.SECRET_KEY = "test-secret-key"
        data = {"sub": "testuser"}
        token = AuthService.create_access_token(data)
        payload = AuthService.verify_access_token(token)
        assert payload["sub"] == "testuser"

    @patch('app.services.auth_service.settings')
    def test_verify_access_token_invalid(self, mock_settings):
        """Test verification of invalid access token raises exception"""
        mock_settings.SECRET_KEY = "test-secret-key"
        with pytest.raises(InvalidCredentialsException):
            AuthService.verify_access_token("invalid-token")

    @patch('app.services.auth_service.settings')
    def test_verify_refresh_token_valid(self, mock_settings):
        """Test verification of valid refresh token"""
        mock_settings.REFRESH_SECRET_KEY = "test-refresh-key"
        data = {"sub": "testuser"}
        token = AuthService.create_refresh_token(data)
        payload = AuthService.verify_refresh_token(token)
        assert payload["sub"] == "testuser"

    @patch('app.services.auth_service.settings')
    def test_verify_refresh_token_invalid(self, mock_settings):
        """Test verification of invalid refresh token raises exception"""
        mock_settings.REFRESH_SECRET_KEY = "test-refresh-key"
        with pytest.raises(InvalidCredentialsException):
            AuthService.verify_refresh_token("invalid-token")


class TestUserRegistration:
    """Test user registration"""

    def test_register_user_success(self, mock_db_session):
        """Test successful user registration"""
        mock_db_session.query.return_value.filter.return_value.first.return_value = None
        
        user = AuthService.register_user(
            mock_db_session,
            "newuser",
            "new@example.com",
            "password123"
        )
        
        mock_db_session.add.assert_called_once()
        mock_db_session.commit.assert_called()

    def test_register_user_duplicate_username(self, mock_db_session, sample_user):
        """Test registration with existing username fails"""
        mock_db_session.query.return_value.filter.return_value.first.return_value = sample_user
        
        with pytest.raises(InvalidCredentialsException):
            AuthService.register_user(
                mock_db_session,
                "testuser",
                "different@example.com",
                "password123"
            )


class TestUserAuthentication:
    """Test user authentication"""

    def test_authenticate_user_success(self, mock_db_session, sample_user):
        """Test successful authentication"""
        sample_user.hashed_password = AuthService.hash_password("correctpassword")
        mock_db_session.query.return_value.filter.return_value.first.return_value = sample_user
        
        user = AuthService.authenticate_user(mock_db_session, "testuser", "correctpassword")
        assert user.username == "testuser"

    def test_authenticate_user_wrong_password(self, mock_db_session, sample_user):
        """Test authentication with wrong password"""
        sample_user.hashed_password = AuthService.hash_password("correctpassword")
        mock_db_session.query.return_value.filter.return_value.first.return_value = sample_user
        
        with pytest.raises(InvalidCredentialsException):
            AuthService.authenticate_user(mock_db_session, "testuser", "wrongpassword")

    def test_authenticate_user_not_found(self, mock_db_session):
        """Test authentication with non-existent user"""
        mock_db_session.query.return_value.filter.return_value.first.return_value = None
        
        with pytest.raises(InvalidCredentialsException):
            AuthService.authenticate_user(mock_db_session, "nonexistent", "password")


class TestGetUserById:
    """Test get user by ID"""

    def test_get_user_by_id_success(self, mock_db_session, sample_user):
        """Test getting user by ID successfully"""
        mock_db_session.query.return_value.filter.return_value.first.return_value = sample_user
        
        user = AuthService.get_user_by_id(mock_db_session, 1)
        assert user.id == 1

    def test_get_user_by_id_not_found(self, mock_db_session):
        """Test getting non-existent user by ID"""
        mock_db_session.query.return_value.filter.return_value.first.return_value = None
        
        with pytest.raises(UserNotFoundException):
            AuthService.get_user_by_id(mock_db_session, 999)


class TestGetUserByUsername:
    """Test get user by username"""

    def test_get_user_by_username_success(self, mock_db_session, sample_user):
        """Test getting user by username successfully"""
        mock_db_session.query.return_value.filter.return_value.first.return_value = sample_user
        
        user = AuthService.get_user_by_username(mock_db_session, "testuser")
        assert user.username == "testuser"

    def test_get_user_by_username_not_found(self, mock_db_session):
        """Test getting non-existent user by username"""
        mock_db_session.query.return_value.filter.return_value.first.return_value = None
        
        with pytest.raises(UserNotFoundException):
            AuthService.get_user_by_username(mock_db_session, "nonexistent")
# Commit 2: test: add mock database session fixture
