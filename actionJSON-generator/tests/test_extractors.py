"""
Tests for content extractors
"""

import pytest
from fluxa.extractors.youtube_extractor import YouTubeExtractor
from fluxa.extractors.web_extractor import WebExtractor
from fluxa.extractors.factory import ExtractorFactory


class TestYouTubeExtractor:
    """Test YouTube extractor"""
    
    def test_extract_video_id_standard_url(self):
        """Test extracting video ID from standard YouTube URL"""
        extractor = YouTubeExtractor()
        url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        video_id = extractor.extract_video_id(url)
        assert video_id == "dQw4w9WgXcQ"
    
    def test_extract_video_id_short_url(self):
        """Test extracting video ID from short YouTube URL"""
        extractor = YouTubeExtractor()
        url = "https://youtu.be/dQw4w9WgXcQ"
        video_id = extractor.extract_video_id(url)
        assert video_id == "dQw4w9WgXcQ"
    
    def test_extract_video_id_embed_url(self):
        """Test extracting video ID from embed URL"""
        extractor = YouTubeExtractor()
        url = "https://www.youtube.com/embed/dQw4w9WgXcQ"
        video_id = extractor.extract_video_id(url)
        assert video_id == "dQw4w9WgXcQ"
    
    def test_extract_video_id_invalid_url(self):
        """Test extracting video ID from invalid URL"""
        extractor = YouTubeExtractor()
        url = "https://www.example.com/video"
        video_id = extractor.extract_video_id(url)
        assert video_id is None


class TestExtractorFactory:
    """Test extractor factory"""
    
    def test_is_youtube_url_standard(self):
        """Test YouTube URL detection for standard URL"""
        assert ExtractorFactory.is_youtube_url("https://www.youtube.com/watch?v=123")
    
    def test_is_youtube_url_short(self):
        """Test YouTube URL detection for short URL"""
        assert ExtractorFactory.is_youtube_url("https://youtu.be/123")
    
    def test_is_not_youtube_url(self):
        """Test YouTube URL detection for non-YouTube URL"""
        assert not ExtractorFactory.is_youtube_url("https://www.example.com/tutorial")


