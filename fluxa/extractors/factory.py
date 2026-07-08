"""
Factory for selecting the appropriate content extractor
"""

from typing import Dict, Any
from .youtube_extractor import YouTubeExtractor
from .web_extractor import WebExtractor


class ExtractorFactory:
    """Factory to route URLs to appropriate extractors"""

    @staticmethod
    def is_youtube_url(url: str) -> bool:
        """Check if URL is a YouTube video"""
        youtube_domains = ['youtube.com', 'youtu.be', 'youtube-nocookie.com']
        return any(domain in url.lower() for domain in youtube_domains)

    @staticmethod
    def extract(url: str, config: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Extract content from URL using appropriate extractor
        
        Args:
            url: Tutorial URL (YouTube or web article)
            config: Optional configuration dictionary
            
        Returns:
            Extracted content and metadata
            
        Raises:
            ValueError: If extraction fails
        """
        if config is None:
            config = {}
        
        if ExtractorFactory.is_youtube_url(url):
            extractor = YouTubeExtractor()
            max_length = config.get('youtube', {}).get('max_transcript_length', 50000)
            return extractor.extract(url, max_length=max_length)
        else:
            timeout = config.get('web', {}).get('timeout', 30)
            max_length = config.get('web', {}).get('max_content_length', 100000)
            extractor = WebExtractor(timeout=timeout)
            return extractor.extract(url, max_length=max_length)


