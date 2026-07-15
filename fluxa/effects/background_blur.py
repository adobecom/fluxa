"""
Background blur (portrait / bokeh) — deterministic ActionJSON builder.

Keeps the subject sharp and blurs the background: select the subject (AI),
invert the selection to the background, Gaussian-blur it, deselect. Render-tested
against the v1 `actionJSON` endpoint.

This is the automatable equivalent of the classic "duplicate → select object →
mask → lens-blur the background" tutorial flow. Lens Blur / Content-Aware fill /
Color Lookup steps from such tutorials are substituted or skipped (the API
ignores LUT presets); a Gaussian blur on the inverted subject selection gives the
same sharp-subject / soft-background result.
"""

from __future__ import annotations

from typing import Any, Dict, List


def build_background_blur_actions(radius: float = 35.0) -> List[Dict[str, Any]]:
    """
    Build background-blur ActionJSON.

    autoCutout (select subject) → inverse (select background) → gaussianBlur the
    background → deselect. The subject stays perfectly sharp.
    """
    return [
        {"_obj": "autoCutout", "sampleAllLayers": False},
        {"_obj": "inverse"},
        {"_obj": "gaussianBlur", "radius": {"_unit": "pixelsUnit", "_value": float(radius)}},
        {
            "_obj": "set",
            "_target": [{"_ref": "channel", "_property": "selection"}],
            "to": {"_enum": "ordinal", "_value": "none"},
        },
    ]
