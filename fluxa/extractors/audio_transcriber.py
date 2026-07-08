"""
Audio-based transcript fallback for YouTube videos without captions.

When a video has captions/subtitles disabled, we download its audio-only
stream with yt-dlp and transcribe it via OpenAI's Whisper API. yt-dlp can
fetch an m4a/webm audio stream directly (no ffmpeg post-processing needed),
and Whisper accepts those formats, so this fallback works without ffmpeg.
"""

from __future__ import annotations

import logging
import os
import tempfile
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)

# Whisper API hard limit is 25 MB per request.
WHISPER_MAX_BYTES = 25 * 1024 * 1024


def download_audio(url: str, out_dir: Optional[str] = None) -> str:
    """
    Download the audio-only stream of a YouTube video.

    Returns the path to the downloaded audio file. Prefers small m4a/webm
    audio formats so no ffmpeg conversion is required.
    """
    import yt_dlp

    out_dir = out_dir or tempfile.mkdtemp(prefix="fluxa_audio_")
    Path(out_dir).mkdir(parents=True, exist_ok=True)
    outtmpl = os.path.join(out_dir, "audio.%(ext)s")

    ydl_opts = {
        # Smallest reasonable audio stream; m4a first (widely Whisper-compatible).
        "format": "bestaudio[ext=m4a]/bestaudio[ext=webm]/bestaudio/best",
        "outtmpl": outtmpl,
        "noplaylist": True,
        "quiet": True,
        "no_warnings": True,
        # Robustness against YouTube 403s / throttling: retry and try multiple
        # player clients (some clients hand out non-throttled format URLs).
        "retries": 5,
        "fragment_retries": 5,
        "extractor_args": {"youtube": {"player_client": ["android", "web", "ios"]}},
        # Do NOT set postprocessors (that path needs ffmpeg).
    }

    logger.info(f"[whisper-fallback] Downloading audio for {url}")
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        downloaded = ydl.prepare_filename(info)

    # prepare_filename returns the templated name; find the actual file on disk.
    if not os.path.exists(downloaded):
        candidates = sorted(Path(out_dir).glob("audio.*"))
        if not candidates:
            raise RuntimeError("Audio download failed: no output file produced.")
        downloaded = str(candidates[0])

    size = os.path.getsize(downloaded)
    logger.info(f"[whisper-fallback] Downloaded audio: {downloaded} ({size/1024/1024:.1f} MB)")
    return downloaded


def transcribe_audio(audio_path: str, api_key: str, model: str = "whisper-1") -> str:
    """Transcribe an audio file to text using OpenAI's Whisper API."""
    from openai import OpenAI

    size = os.path.getsize(audio_path)
    if size > WHISPER_MAX_BYTES:
        raise ValueError(
            f"Audio is {size/1024/1024:.1f} MB, over the {WHISPER_MAX_BYTES/1024/1024:.0f} MB "
            "Whisper limit. Use a shorter tutorial video or a captioned one."
        )

    client = OpenAI(api_key=api_key)
    logger.info(f"[whisper-fallback] Transcribing {audio_path} with model={model}")
    with open(audio_path, "rb") as f:
        result = client.audio.transcriptions.create(
            model=model,
            file=f,
            response_format="text",
            # These are English Photoshop tutorials; pinning the language prevents
            # Whisper from mis-detecting faint narration as another language.
            language="en",
            prompt="Photoshop tutorial. Steps: select subject, layer, mask, blend mode, filter, adjustment.",
        )
    text = result if isinstance(result, str) else getattr(result, "text", str(result))
    logger.info(f"[whisper-fallback] Transcription complete: {len(text)} characters")
    return text.strip()


def transcribe_from_youtube(url: str, api_key: str, model: str = "whisper-1") -> str:
    """
    Full fallback: download a video's audio and transcribe it to text.

    Raises ValueError/RuntimeError on failure so callers can surface a clear
    message to the user.
    """
    audio_path = download_audio(url)
    try:
        return transcribe_audio(audio_path, api_key=api_key, model=model)
    finally:
        # Best-effort cleanup of the temp audio file and its directory.
        try:
            parent = Path(audio_path).parent
            os.remove(audio_path)
            if parent.name.startswith("fluxa_audio_") and not any(parent.iterdir()):
                parent.rmdir()
        except Exception:
            pass
