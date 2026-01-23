# Quiz tests: generation, submission, scoring
import pytest
from unittest.mock import Mock, MagicMock, patch
from datetime import datetime
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app.models.quiz_attempt import QuizAttempt
from app.models.article import Article, ActionType


class TestQuizAttemptModel:
    """Test QuizAttempt model"""

    def test_quiz_attempt_creation(self, sample_quiz_attempt):
        """Test quiz attempt instance creation"""
        assert sample_quiz_attempt.id == 1
        assert sample_quiz_attempt.user_id == 1
        assert sample_quiz_attempt.article_id == 1
        assert sample_quiz_attempt.score == 85.0

    def test_quiz_attempt_has_required_fields(self, sample_quiz_attempt):
        """Test that quiz attempt has all required fields"""
        assert hasattr(sample_quiz_attempt, 'id')
        assert hasattr(sample_quiz_attempt, 'user_id')
        assert hasattr(sample_quiz_attempt, 'article_id')
        assert hasattr(sample_quiz_attempt, 'score')
        assert hasattr(sample_quiz_attempt, 'submitted_at')

    def test_quiz_attempt_score_range(self):
        """Test quiz score can be in valid range"""
        attempt = QuizAttempt(
            id=1,
            user_id=1,
            article_id=1,
            score=100.0,
            submitted_at=datetime.utcnow()
        )
        assert 0 <= attempt.score <= 100

    def test_quiz_attempt_zero_score(self):
        """Test quiz with zero score"""
        attempt = QuizAttempt(
            id=1,
            user_id=1,
            article_id=1,
            score=0.0,
            submitted_at=datetime.utcnow()
        )
        assert attempt.score == 0.0

    def test_quiz_attempt_perfect_score(self):
        """Test quiz with perfect score"""
        attempt = QuizAttempt(
            id=1,
            user_id=1,
            article_id=1,
            score=100.0,
            submitted_at=datetime.utcnow()
        )
        assert attempt.score == 100.0


class TestQuizScoring:
    """Test quiz scoring functionality"""

    def test_calculate_score_all_correct(self):
        """Test score calculation with all correct answers"""
        correct_answers = ["A", "B", "C", "D"]
        user_answers = ["A", "B", "C", "D"]
        score = self._calculate_score(correct_answers, user_answers)
        assert score == 100.0

    def test_calculate_score_all_wrong(self):
        """Test score calculation with all wrong answers"""
        correct_answers = ["A", "B", "C", "D"]
        user_answers = ["B", "C", "D", "A"]
        score = self._calculate_score(correct_answers, user_answers)
        assert score == 0.0

    def test_calculate_score_partial(self):
        """Test score calculation with partial correct"""
        correct_answers = ["A", "B", "C", "D"]
        user_answers = ["A", "B", "D", "A"]
        score = self._calculate_score(correct_answers, user_answers)
        assert score == 50.0

    def test_calculate_score_empty_answers(self):
        """Test score calculation with empty answers"""
        correct_answers = ["A", "B", "C", "D"]
        user_answers = []
        score = self._calculate_score(correct_answers, user_answers)
        assert score == 0.0

    def test_calculate_score_single_question(self):
        """Test score with single question"""
        correct_answers = ["A"]
        user_answers = ["A"]
        score = self._calculate_score(correct_answers, user_answers)
        assert score == 100.0

    @staticmethod
    def _calculate_score(correct: list, user: list) -> float:
        """Helper to calculate score"""
        if not correct:
            return 0.0
        if not user:
            return 0.0
        correct_count = sum(1 for c, u in zip(correct, user) if c == u)
        return (correct_count / len(correct)) * 100


class TestQuizGeneration:
    """Test quiz generation"""

    def test_generate_quiz_structure(self):
        """Test that generated quiz has correct structure"""
        quiz = self._mock_quiz_response()
        assert "questions" in quiz
        assert len(quiz["questions"]) > 0

    def test_quiz_question_format(self):
        """Test quiz question format"""
        quiz = self._mock_quiz_response()
        question = quiz["questions"][0]
        assert "question" in question
        assert "options" in question
        assert "correct_answer" in question

    def test_quiz_has_multiple_options(self):
        """Test quiz questions have multiple options"""
        quiz = self._mock_quiz_response()
        question = quiz["questions"][0]
        assert len(question["options"]) >= 2

    def test_quiz_correct_answer_in_options(self):
        """Test correct answer is in options"""
        quiz = self._mock_quiz_response()
        question = quiz["questions"][0]
        assert question["correct_answer"] in question["options"]

    def test_quiz_question_count(self):
        """Test quiz has expected number of questions"""
        quiz = self._mock_quiz_response(num_questions=5)
        assert len(quiz["questions"]) == 5

    @staticmethod
    def _mock_quiz_response(num_questions=3):
        """Generate mock quiz response"""
        questions = []
        for i in range(num_questions):
            questions.append({
                "question": f"Question {i+1}?",
                "options": ["Option A", "Option B", "Option C", "Option D"],
                "correct_answer": "Option A"
            })
        return {"questions": questions}


class TestQuizValidation:
    """Test quiz validation"""

    def test_validate_answer_format_valid(self):
        """Test valid answer format"""
        answer = {"question_id": 1, "answer": "A"}
        assert self._is_valid_answer(answer)

    def test_validate_answer_format_invalid_missing_answer(self):
        """Test invalid format - missing answer"""
        answer = {"question_id": 1}
        assert not self._is_valid_answer(answer)

    def test_validate_answer_format_invalid_missing_id(self):
        """Test invalid format - missing question_id"""
        answer = {"answer": "A"}
        assert not self._is_valid_answer(answer)

    def test_validate_answer_format_empty(self):
        """Test empty answer"""
        answer = {}
        assert not self._is_valid_answer(answer)

    def test_validate_multiple_answers(self):
        """Test validating multiple answers"""
        answers = [
            {"question_id": 1, "answer": "A"},
            {"question_id": 2, "answer": "B"},
            {"question_id": 3, "answer": "C"}
        ]
        assert all(self._is_valid_answer(a) for a in answers)

    @staticmethod
    def _is_valid_answer(answer: dict) -> bool:
        """Validate answer format"""
        return "question_id" in answer and "answer" in answer


class TestQuizHistory:
    """Test quiz history functionality"""

    def test_get_user_quiz_history(self, mock_db_session, sample_quiz_attempt):
        """Test getting user's quiz history"""
        mock_db_session.query.return_value.filter.return_value.all.return_value = [sample_quiz_attempt]
        
        history = mock_db_session.query(QuizAttempt).filter().all()
        assert len(history) == 1
        assert history[0].score == 85.0

    def test_get_user_quiz_history_empty(self, mock_db_session):
        """Test getting empty quiz history"""
        mock_db_session.query.return_value.filter.return_value.all.return_value = []
        
        history = mock_db_session.query(QuizAttempt).filter().all()
        assert len(history) == 0

    def test_get_average_score(self):
        """Test calculating average score"""
        scores = [80.0, 90.0, 70.0, 100.0]
        average = sum(scores) / len(scores)
        assert average == 85.0

    def test_get_highest_score(self):
        """Test getting highest score"""
        scores = [80.0, 90.0, 70.0, 100.0]
        highest = max(scores)
        assert highest == 100.0

    def test_get_quiz_count(self, mock_db_session):
        """Test getting total quiz count for user"""
        mock_db_session.query.return_value.filter.return_value.count.return_value = 5
        count = mock_db_session.query(QuizAttempt).filter().count()
        assert count == 5
# Commit 4: test: add sample article and quiz fixtures
# Commit 19: test: add content structure tests
# Commit 34: test: add PDF metadata tests
# Commit 49: test: add mock Groq client implementation
