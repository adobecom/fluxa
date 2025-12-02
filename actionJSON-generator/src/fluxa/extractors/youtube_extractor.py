"""
YouTube video transcript extractor
"""

import re
from typing import Optional, Dict, Any
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import (
    TranscriptsDisabled,
    NoTranscriptFound,
    VideoUnavailable,
)


class YouTubeExtractor:
    """Extract transcript and metadata from YouTube videos"""

    @staticmethod
    def extract_video_id(url: str) -> Optional[str]:
        """
        Extract video ID from various YouTube URL formats
        
        Args:
            url: YouTube URL
            
        Returns:
            Video ID or None if not found
        """
        patterns = [
            r'(?:https?:\/\/)?(?:www\.)?youtube\.com\/watch\?v=([^&]+)',
            r'(?:https?:\/\/)?(?:www\.)?youtu\.be\/([^?]+)',
            r'(?:https?:\/\/)?(?:www\.)?youtube\.com\/embed\/([^?]+)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        
        return None

    def extract(self, url: str, max_length: int = 50000) -> Dict[str, Any]:
        """
        Extract transcript from YouTube video
        
        Args:
            url: YouTube video URL
            max_length: Maximum transcript length
            
        Returns:
            Dictionary with content and metadata
            
        Raises:
            ValueError: If video ID cannot be extracted or transcript unavailable
        """
        video_id = self.extract_video_id(url)
        if not video_id:
            raise ValueError(f"Could not extract video ID from URL: {url}")

        try:
            # Get transcript
            transcript_list = YouTubeTranscriptApi().fetch(video_id)
            
            # Combine transcript segments
            full_text = " ".join([entry.text for entry in transcript_list])
            
            # Truncate if too long
            if len(full_text) > max_length:
                full_text = full_text[:max_length] + "... [truncated]"
            
            return {
                "content": full_text,
                "source": url,
                "video_id": video_id,
                "type": "youtube",
                "segment_count": len(transcript_list),
            }
            
        except TranscriptsDisabled:
            raise ValueError(
                f"Transcripts are disabled for video: {video_id}. "
                "Try a different video or use a web article instead."
            )
        except NoTranscriptFound:
            raise ValueError(
                f"No transcript found for video: {video_id}. "
                "The video may not have captions available."
            )
        except VideoUnavailable:
            raise ValueError(f"Video unavailable: {video_id}")
        except Exception as e:
            raise ValueError(f"Error extracting YouTube transcript: {str(e)}")


