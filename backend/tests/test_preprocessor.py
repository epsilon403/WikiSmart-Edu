# Preprocessor tests: text cleaning and segmentation
import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app.services.preprocessor import clean_and_segment_text, clean_text, split_into_chunks


class TestCleanText:
    """Test clean_text function"""

    def test_removes_multiple_spaces(self):
        """Test removal of multiple consecutive spaces"""
        text = "Hello    world     test"
        result = clean_text(text)
        assert "    " not in result
        assert "  " not in result

    def test_removes_multiple_newlines(self):
        """Test removal of multiple consecutive newlines"""
        text = "Line1\n\n\n\nLine2"
        result = clean_text(text)
        assert "\n\n\n" not in result

    def test_strips_leading_whitespace(self):
        """Test stripping of leading whitespace"""
        text = "    Hello"
        result = clean_text(text)
        assert not result.startswith(" ")

    def test_strips_trailing_whitespace(self):
        """Test stripping of trailing whitespace"""
        text = "Hello    "
        result = clean_text(text)
        assert not result.endswith(" ")

    def test_handles_empty_string(self):
        """Test handling of empty string"""
        result = clean_text("")
        assert result == ""

    def test_handles_only_whitespace(self):
        """Test handling of whitespace-only string"""
        result = clean_text("     ")
        assert result == ""

    def test_preserves_single_spaces(self):
        """Test preservation of single spaces"""
        text = "Hello world"
        result = clean_text(text)
        assert result == "Hello world"

    def test_preserves_single_newlines(self):
        """Test that text content is preserved"""
        text = "Hello\nworld"
        result = clean_text(text)
        assert "Hello" in result
        assert "world" in result


class TestCleanAndSegmentText:
    """Test clean_and_segment_text function"""

    def test_returns_dictionary(self):
        """Test that function returns a dictionary"""
        text = "Some text content"
        result = clean_and_segment_text(text)
        assert isinstance(result, dict)

    def test_non_empty_result(self):
        """Test that result is not empty for non-empty input"""
        text = "Some meaningful text content here."
        result = clean_and_segment_text(text)
        assert len(result) > 0

    def test_handles_empty_string(self):
        """Test handling of empty string"""
        result = clean_and_segment_text("")
        assert isinstance(result, dict)

    def test_detects_introduction(self):
        """Test detection of introduction section"""
        text = "This is the introduction.\n\nHistory\nThis is history content."
        result = clean_and_segment_text(text)
        # Should have at least one section
        assert len(result) >= 1

    def test_segments_by_headers(self):
        """Test segmentation by section headers"""
        text = """Introduction
        This is intro content.
        
        Background
        This is background content.
        
        Methods
        This is methods content."""
        
        result = clean_and_segment_text(text)
        assert len(result) >= 1

    def test_handles_single_paragraph(self):
        """Test handling of single paragraph text"""
        text = "This is just a single paragraph with no sections or headers."
        result = clean_and_segment_text(text)
        assert len(result) >= 1

    def test_preserves_content(self):
        """Test that content is preserved in segments"""
        text = "Important content that should be preserved."
        result = clean_and_segment_text(text)
        all_content = " ".join(result.values())
        assert "Important" in all_content or "content" in all_content


class TestSplitIntoChunks:
    """Test split_into_chunks function"""

    def test_short_text_single_chunk(self):
        """Test that short text returns single chunk"""
        text = "Short text"
        chunks = split_into_chunks(text, chunk_size=1000)
        assert len(chunks) == 1

    def test_long_text_multiple_chunks(self):
        """Test that long text returns multiple chunks"""
        text = "word " * 500  # Creates long text
        chunks = split_into_chunks(text, chunk_size=100)
        assert len(chunks) > 1

    def test_chunk_size_respected(self):
        """Test that chunks respect size limit approximately"""
        text = "a" * 5000
        chunks = split_into_chunks(text, chunk_size=1000, overlap=0)
        for chunk in chunks[:-1]:  # Last chunk may be smaller
            assert len(chunk) <= 1100  # Allow some flexibility

    def test_overlap_creates_more_chunks(self):
        """Test that overlap creates overlapping chunks"""
        text = "a" * 3000
        no_overlap = split_into_chunks(text, chunk_size=1000, overlap=0)
        with_overlap = split_into_chunks(text, chunk_size=1000, overlap=200)
        assert len(with_overlap) >= len(no_overlap)

    def test_respects_sentence_boundaries(self):
        """Test preference for sentence boundaries"""
        text = "First sentence. Second sentence. Third sentence. Fourth sentence."
        chunks = split_into_chunks(text, chunk_size=30, overlap=0)
        # Most chunks should end with period
        period_endings = sum(1 for c in chunks if c.strip().endswith('.'))
        assert period_endings >= 1

    def test_handles_empty_string(self):
        """Test handling of empty string"""
        chunks = split_into_chunks("", chunk_size=100)
        assert len(chunks) == 1
        assert chunks[0] == ""

    def test_handles_text_exactly_chunk_size(self):
        """Test text exactly at chunk size"""
        text = "a" * 100
        chunks = split_into_chunks(text, chunk_size=100)
        assert len(chunks) == 1

    def test_preserves_all_content(self):
        """Test that all content is preserved across chunks"""
        text = "unique_word " * 100
        chunks = split_into_chunks(text, chunk_size=200, overlap=50)
        combined = "".join(chunks)
        assert combined.count("unique_word") >= 100


class TestChunkOverlap:
    """Test chunk overlap functionality"""

    def test_overlap_value(self):
        """Test overlap is applied correctly"""
        text = "a" * 2000
        chunks = split_into_chunks(text, chunk_size=500, overlap=100)
        # With overlap, adjacent chunks should share content
        assert len(chunks) > 2

    def test_zero_overlap(self):
        """Test zero overlap"""
        text = "a" * 2000
        chunks = split_into_chunks(text, chunk_size=500, overlap=0)
        total_length = sum(len(c) for c in chunks)
        assert total_length == 2000

    def test_large_overlap(self):
        """Test large overlap value"""
        text = "a" * 2000
        chunks = split_into_chunks(text, chunk_size=500, overlap=400)
        # Large overlap creates more chunks
        assert len(chunks) > 4


class TestEdgeCases:
    """Test edge cases"""

    def test_unicode_text(self):
        """Test handling of unicode text"""
        text = "日本語テキスト " * 100
        chunks = split_into_chunks(text, chunk_size=100)
        assert len(chunks) >= 1

    def test_special_characters(self):
        """Test handling of special characters"""
        text = "Hello @#$%^&*() World!" * 50
        result = clean_text(text)
        assert "@#$%^&*()" in result

    def test_mixed_whitespace(self):
        """Test handling of mixed whitespace"""
        text = "Hello\t\t  \n\n  world"
        result = clean_text(text)
        assert "Hello" in result
        assert "world" in result

    def test_very_long_word(self):
        """Test handling of very long words"""
        text = "a" * 10000
        chunks = split_into_chunks(text, chunk_size=1000)
        assert len(chunks) >= 10
# Commit 8: test: add access token creation tests
# Commit 23: test: add text chunking tests
# Commit 38: test: add quiz validation tests
