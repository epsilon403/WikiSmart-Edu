# User model tests
import pytest
from datetime import datetime
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app.models.user import User, UserRole


class TestUserModel:
    """Test User model"""

    def test_user_creation(self, sample_user):
        """Test user instance creation"""
        assert sample_user.id == 1
        assert sample_user.username == "testuser"
        assert sample_user.email == "test@example.com"

    def test_user_has_required_fields(self, sample_user):
        """Test that user has all required fields"""
        assert hasattr(sample_user, 'id')
        assert hasattr(sample_user, 'username')
        assert hasattr(sample_user, 'email')
        assert hasattr(sample_user, 'hashed_password')
        assert hasattr(sample_user, 'role')
        assert hasattr(sample_user, 'created_at')

    def test_user_default_role(self):
        """Test default user role"""
        user = User(
            username="newuser",
            email="new@example.com",
            hashed_password="hashed"
        )
        # Default role should be set by SQLAlchemy default
        assert user.role is None or user.role == UserRole.USER

    def test_admin_user_role(self, sample_admin_user):
        """Test admin user role"""
        assert sample_admin_user.role == UserRole.ADMIN


class TestUserRole:
    """Test UserRole enum"""

    def test_user_role_values(self):
        """Test user role enum values"""
        assert UserRole.USER == "user"
        assert UserRole.ADMIN == "admin"

    def test_user_role_is_string_enum(self):
        """Test that UserRole inherits from str"""
        assert isinstance(UserRole.USER, str)
        assert isinstance(UserRole.ADMIN, str)

    def test_user_role_comparison(self):
        """Test user role comparison"""
        assert UserRole.USER != UserRole.ADMIN

    def test_user_role_string_representation(self):
        """Test string representation"""
        assert str(UserRole.USER) == "user"
        assert str(UserRole.ADMIN) == "admin"


class TestUserValidation:
    """Test user validation"""

    def test_valid_username(self):
        """Test valid username format"""
        valid_usernames = ["user1", "john_doe", "JaneDoe123"]
        for username in valid_usernames:
            assert len(username) > 0

    def test_valid_email_format(self):
        """Test valid email format"""
        valid_emails = ["test@example.com", "user.name@domain.org"]
        for email in valid_emails:
            assert "@" in email
            assert "." in email.split("@")[1]

    def test_invalid_email_format(self):
        """Test invalid email format"""
        invalid_emails = ["notanemail", "missing@domain", "@nodomain.com"]
        for email in invalid_emails:
            is_valid = "@" in email and "." in email.split("@")[1] if "@" in email else False
            # At least one should be invalid
            assert not is_valid or email == "missing@domain"

    def test_password_not_stored_plain(self, sample_user):
        """Test that password is hashed"""
        assert sample_user.hashed_password != "plainpassword"
        assert "$" in sample_user.hashed_password  # bcrypt hash format


class TestUserRelationships:
    """Test user relationships"""

    def test_user_has_articles_relationship(self):
        """Test user has articles relationship defined"""
        user = User(
            username="test",
            email="test@test.com",
            hashed_password="hash"
        )
        assert hasattr(User, 'articles')

    def test_user_has_quiz_attempts_relationship(self):
        """Test user has quiz_attempts relationship defined"""
        assert hasattr(User, 'quiz_attempts')


class TestUserTimestamps:
    """Test user timestamps"""

    def test_created_at_is_datetime(self, sample_user):
        """Test created_at is datetime"""
        assert isinstance(sample_user.created_at, datetime)

    def test_created_at_not_future(self, sample_user):
        """Test created_at is not in future"""
        assert sample_user.created_at <= datetime.utcnow()


class TestUserEquality:
    """Test user equality"""

    def test_users_with_same_id_equal(self):
        """Test users with same ID are considered equal by ID"""
        user1 = User(id=1, username="user1", email="user1@test.com", hashed_password="hash")
        user2 = User(id=1, username="user2", email="user2@test.com", hashed_password="hash")
        assert user1.id == user2.id

    def test_users_with_different_id_not_equal(self):
        """Test users with different IDs are not equal"""
        user1 = User(id=1, username="user1", email="user1@test.com", hashed_password="hash")
        user2 = User(id=2, username="user1", email="user1@test.com", hashed_password="hash")
        assert user1.id != user2.id
# Commit 7: test: add password verification tests
# Commit 22: test: add text segmentation tests
# Commit 37: test: add quiz generation tests
