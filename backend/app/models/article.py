# Article model: id, url, title, action, created_at, user_id
import enum
from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, Enum, DateTime
from sqlalchemy.orm import relationship
from ..database import Base

class ActionType(str, enum.Enum):
    SUMMARY = "summary"
    TRANSLATION = "translation"
    QUIZ = "quiz"

class Article(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    url = Column(String, nullable=False)
    title = Column(String, nullable=False)
    action = Column(Enum(ActionType), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="articles")
    quiz_attempts = relationship("QuizAttempt", back_populates="article", cascade="all, delete-orphan")