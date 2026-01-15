"""Custom exceptions and centralized exception management"""

class AppException(Exception):
    """Base application exception"""
    def __init__(self, detail: str, status_code: int = 400):
        self.detail = detail
        self.status_code = status_code
        super().__init__(self.detail)


class InvalidCredentialsException(AppException):
    """Exception raised when credentials are invalid"""
    def __init__(self, detail: str = "Invalid credentials"):
        super().__init__(detail, status_code=401)


class UserNotFoundException(AppException):
    """Exception raised when user is not found"""
    def __init__(self, detail: str = "User not found"):
        super().__init__(detail, status_code=404)
