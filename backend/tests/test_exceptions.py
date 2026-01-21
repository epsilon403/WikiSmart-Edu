# Exception tests
import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app.core.exceptions import AppException, InvalidCredentialsException, UserNotFoundException


class TestAppException:
    """Test base AppException"""

    def test_app_exception_creation(self):
        """Test AppException instance creation"""
        exc = AppException("Test error")
        assert exc.detail == "Test error"
        assert exc.status_code == 400

    def test_app_exception_custom_status(self):
        """Test AppException with custom status code"""
        exc = AppException("Test error", status_code=500)
        assert exc.status_code == 500

    def test_app_exception_inheritance(self):
        """Test AppException inherits from Exception"""
        exc = AppException("Test")
        assert isinstance(exc, Exception)

    def test_app_exception_str(self):
        """Test AppException string representation"""
        exc = AppException("Test error message")
        assert "Test error message" in str(exc)


class TestInvalidCredentialsException:
    """Test InvalidCredentialsException"""

    def test_default_message(self):
        """Test default error message"""
        exc = InvalidCredentialsException()
        assert exc.detail == "Invalid credentials"

    def test_custom_message(self):
        """Test custom error message"""
        exc = InvalidCredentialsException("Custom error")
        assert exc.detail == "Custom error"

    def test_status_code(self):
        """Test status code is 401"""
        exc = InvalidCredentialsException()
        assert exc.status_code == 401

    def test_inheritance(self):
        """Test inheritance from AppException"""
        exc = InvalidCredentialsException()
        assert isinstance(exc, AppException)


class TestUserNotFoundException:
    """Test UserNotFoundException"""

    def test_default_message(self):
        """Test default error message"""
        exc = UserNotFoundException()
        assert exc.detail == "User not found"

    def test_custom_message(self):
        """Test custom error message"""
        exc = UserNotFoundException("User john not found")
        assert exc.detail == "User john not found"

    def test_status_code(self):
        """Test status code is 404"""
        exc = UserNotFoundException()
        assert exc.status_code == 404

    def test_inheritance(self):
        """Test inheritance from AppException"""
        exc = UserNotFoundException()
        assert isinstance(exc, AppException)


class TestExceptionRaising:
    """Test exception raising behavior"""

    def test_raise_app_exception(self):
        """Test raising AppException"""
        with pytest.raises(AppException):
            raise AppException("Test")

    def test_raise_invalid_credentials(self):
        """Test raising InvalidCredentialsException"""
        with pytest.raises(InvalidCredentialsException):
            raise InvalidCredentialsException()

    def test_raise_user_not_found(self):
        """Test raising UserNotFoundException"""
        with pytest.raises(UserNotFoundException):
            raise UserNotFoundException()

    def test_catch_as_base_exception(self):
        """Test catching as base Exception"""
        with pytest.raises(Exception):
            raise InvalidCredentialsException()


class TestExceptionDetails:
    """Test exception detail attributes"""

    def test_detail_attribute(self):
        """Test detail attribute exists"""
        exc = AppException("Test")
        assert hasattr(exc, 'detail')

    def test_status_code_attribute(self):
        """Test status_code attribute exists"""
        exc = AppException("Test")
        assert hasattr(exc, 'status_code')

    def test_detail_is_string(self):
        """Test detail is string"""
        exc = AppException("Test message")
        assert isinstance(exc.detail, str)

    def test_status_code_is_int(self):
        """Test status_code is integer"""
        exc = AppException("Test")
        assert isinstance(exc.status_code, int)
# Commit 9: test: add refresh token creation tests
# Commit 24: test: add preprocessor edge case tests
# Commit 39: test: add quiz history tests
