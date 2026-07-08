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
            r'(?:https?:\/\/)?(?:www\.)?youtu\.be\/([^?&\/]+)',
            r'(?:https?:\/\/)?(?:www\.)?youtube\.com\/embed\/([^?&\/]+)',
            r'(?:https?:\/\/)?(?:www\.)?youtube\.com\/shorts\/([^?&\/]+)',
            r'(?:https?:\/\/)?(?:www\.)?youtube\.com\/live\/([^?&\/]+)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        
        return None

    def extract(
        self,
        url: str,
        max_length: int = 50000,
        whisper_api_key: Optional[str] = None,
        whisper_model: str = "whisper-1",
    ) -> Dict[str, Any]:
        """
        Extract transcript from YouTube video.

        Resolution order (most reliable first):
          1. Caption track via yt-dlp (manual subs preferred, then auto).
          2. `youtube-transcript-api` (legacy scraper; often blocked).
          3. Whisper audio transcription (if `whisper_api_key` is provided).

        Args:
            url: YouTube video URL
            max_length: Maximum transcript length
            whisper_api_key: OpenAI API key enabling the audio fallback
            whisper_model: Whisper model to use for the audio fallback

        Returns:
            Dictionary with content and metadata

        Raises:
            ValueError: If video ID cannot be extracted or no transcript is obtainable
        """
        video_id = self.extract_video_id(url)
        if not video_id:
            raise ValueError(f"Could not extract video ID from URL: {url}")

        # 1) Primary: real caption track via yt-dlp (robust).
        try:
            from .caption_extractor import fetch_captions

            caption_text = fetch_captions(url, max_length=max_length)
            if caption_text:
                return {
                    "content": caption_text,
                    "source": url,
                    "video_id": video_id,
                    "type": "youtube",
                    "segment_count": None,
                }
        except Exception as e:
            # Non-fatal: fall through to the other methods.
            import logging

            logging.getLogger(__name__).warning(f"yt-dlp caption fetch failed: {e}")

        # 2) Secondary: legacy youtube-transcript-api scraper.
        try:
            transcript_list = YouTubeTranscriptApi().fetch(video_id)
            full_text = " ".join([entry.text for entry in transcript_list])
            if len(full_text) > max_length:
                full_text = full_text[:max_length] + "... [truncated]"
            return {
                "content": full_text,
                "source": url,
                "video_id": video_id,
                "type": "youtube",
                "segment_count": len(transcript_list),
            }
        except (TranscriptsDisabled, NoTranscriptFound):
            # 3) Last resort: Whisper audio transcription.
            if whisper_api_key:
                return self._extract_via_audio(
                    url, video_id, max_length, whisper_api_key, whisper_model
                )
            raise ValueError(
                f"No captions found for video {video_id} (and no OpenAI key was "
                "available for the audio-transcription fallback). Try a tutorial "
                "that has captions."
            )
        except VideoUnavailable:
            raise ValueError(f"Video unavailable: {video_id}")
        except Exception as e:
            # If the scraper errors but Whisper is available, still try audio.
            if whisper_api_key:
                return self._extract_via_audio(
                    url, video_id, max_length, whisper_api_key, whisper_model
                )
            raise ValueError(f"Error extracting YouTube transcript: {str(e)}")

    def _extract_via_audio(
        self,
        url: str,
        video_id: str,
        max_length: int,
        whisper_api_key: str,
        whisper_model: str,
    ) -> Dict[str, Any]:
        """Fallback: transcribe the video's audio with Whisper when captions are missing."""
        from .audio_transcriber import transcribe_from_youtube

        try:
            full_text = transcribe_from_youtube(url, api_key=whisper_api_key, model=whisper_model)
        except Exception as e:
            raise ValueError(
                f"No captions for video {video_id}, and audio transcription "
                f"fallback failed: {e}"
            )

        if not full_text.strip():
            raise ValueError(
                f"Audio transcription for video {video_id} produced no text "
                "(the video may have no speech)."
            )

        if len(full_text) > max_length:
            full_text = full_text[:max_length] + "... [truncated]"

        return {
            "content": full_text,
            "source": url,
            "video_id": video_id,
            "type": "youtube_audio",
            "segment_count": None,
        }


