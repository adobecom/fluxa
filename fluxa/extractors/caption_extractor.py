"""
Robust YouTube caption extraction via yt-dlp.

`youtube-transcript-api` frequently returns `TranscriptsDisabled` when YouTube
rate-limits/blocks the request, even for videos that clearly have captions.
yt-dlp reads the same caption tracks far more reliably (and we already depend on
it for the Whisper audio fallback). This module fetches the real caption track
(manual subtitles preferred, then auto-generated) and returns plain text.
"""

from __future__ import annotations

import json
import logging
import urllib.request
from typing import List, Optional

logger = logging.getLogger(__name__)

# Common English track keys, in order of preference. Manual subtitle tracks are
# checked before automatic ones. Auto-translated tracks look like "fr-en-GB" and
# are intentionally NOT matched here — we only want the native caption.
_EN_KEYS = ["en", "en-US", "en-GB", "en-orig", "a.en"]


def _pick_track(tracks: dict, prefer: List[str]) -> Optional[list]:
    """Return the caption format list for the best-matching language key."""
    if not tracks:
        return None
    # Exact preferred matches first.
    for key in prefer:
        if key in tracks:
            return tracks[key]
    # Any key that starts with "en" but is not an auto-translation (no leading
    # "<srclang>-" prefix, i.e. it starts with "en").
    for key in tracks:
        if key.lower().startswith("en"):
            return tracks[key]
    return None


def _download_track_text(formats: list) -> Optional[str]:
    """Download a caption track (prefer json3) and flatten it to plain text."""
    # Prefer json3 (clean structured events); fall back to vtt/srv1.
    by_ext = {f.get("ext"): f for f in formats}
    for ext in ("json3", "srv1", "vtt", "srv3", "srv2"):
        fmt = by_ext.get(ext)
        if not fmt or not fmt.get("url"):
            continue
        try:
            raw = urllib.request.urlopen(fmt["url"], timeout=30).read().decode("utf-8", "ignore")
        except Exception as e:
            logger.warning(f"[captions] failed to download {ext} track: {e}")
            continue

        if ext == "json3":
            text = _parse_json3(raw)
        else:
            text = _parse_timed_text(raw)
        if text:
            return text
    return None


def _parse_json3(raw: str) -> str:
    data = json.loads(raw)
    parts = []
    for ev in data.get("events", []):
        if "segs" in ev:
            parts.append("".join(s.get("utf8", "") for s in ev["segs"]))
    return " ".join(" ".join(p.split()) for p in parts if p.strip()).strip()


def _parse_timed_text(raw: str) -> str:
    """Very small vtt/srv1 flattener: strip tags/timestamps, keep spoken text."""
    import re

    lines = []
    for line in raw.splitlines():
        line = line.strip()
        if not line:
            continue
        # Skip WEBVTT header, cue numbers, and timestamp lines.
        if line.upper().startswith("WEBVTT") or line.isdigit() or "-->" in line:
            continue
        # Strip XML/VTT tags like <c>, <00:00:01.000>, <text ...>.
        line = re.sub(r"<[^>]+>", "", line)
        if line:
            lines.append(line)
    return " ".join(" ".join(lines).split()).strip()


def fetch_captions(url: str, max_length: int = 50000) -> Optional[str]:
    """
    Fetch a YouTube video's caption transcript via yt-dlp.

    Returns the caption text (manual subtitles preferred, else auto-generated),
    or None if the video has no usable English caption track.
    """
    import yt_dlp

    ydl_opts = {
        "quiet": True,
        "no_warnings": True,
        "skip_download": True,
        "writesubtitles": True,
        "writeautomaticsub": True,
        # CRITICAL: for `watch?v=X&list=...` URLs, only process video X. Without
        # this, yt-dlp follows the playlist and may resolve a different (or
        # private) video, causing spurious failures.
        "noplaylist": True,
        "extractor_args": {"youtube": {"player_client": ["android", "web", "ios"]}},
    }
    logger.info(f"[captions] Fetching caption tracks via yt-dlp for {url}")
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)

    manual = info.get("subtitles") or {}
    auto = info.get("automatic_captions") or {}

    # Manual (human) captions first — highest quality.
    track = _pick_track(manual, _EN_KEYS)
    source = "manual"
    if not track:
        track = _pick_track(auto, _EN_KEYS)
        source = "auto"
    if not track:
        logger.info("[captions] No English caption track found.")
        return None

    text = _download_track_text(track)
    if not text:
        logger.info("[captions] Caption track found but could not be parsed.")
        return None

    logger.info(f"[captions] Extracted {len(text)} chars from {source} captions.")
    if len(text) > max_length:
        text = text[:max_length] + "... [truncated]"
    return text
