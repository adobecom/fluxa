"""
Text-behind-subject ("embed text") — deterministic ActionJSON builder.

The polished effect (as in the tutorials) is a TWO-layer "wrap":
  1. A big SOLID word BEHIND the subject (between subject and background) — the
     subject occludes it where they overlap.
  2. An identical word ON TOP of the subject with **fill 0% + white stroke**, so
     over the subject you see only the outline.
Together they read as text wrapping around the person/object.

The user supplies the actual word (asked for in the pipeline); no placeholder text.
"""

from __future__ import annotations

from typing import Any, Dict, List


def _target_current() -> List[Dict[str, Any]]:
    return [{"_enum": "ordinal", "_ref": "layer", "_value": "targetEnum"}]


def _select_ordinal(value: str) -> Dict[str, Any]:
    return {"_obj": "select", "_target": [{"_enum": "ordinal", "_ref": "layer", "_value": value}]}


def _make_text_layer(text: str, font: str, size_px: int, color_rgb: tuple) -> Dict[str, Any]:
    n = len(text)
    r, g, b = color_rgb
    return {
        "_obj": "make",
        "_target": [{"_ref": "textLayer"}],
        "using": {
            "_obj": "textLayer",
            "textKey": text,
            "textClickPoint": {
                "_obj": "paint",
                "horizontal": {"_unit": "percentUnit", "_value": 50.0},
                "vertical": {"_unit": "percentUnit", "_value": 50.0},
            },
            "textStyleRange": [
                {
                    "_obj": "textStyleRange",
                    "from": 0,
                    "to": n,
                    "textStyle": {
                        "_obj": "textStyle",
                        "fontPostScriptName": font,
                        "size": {"_unit": "pixelsUnit", "_value": size_px},
                        "color": {"_obj": "RGBColor", "red": r, "grain": g, "blue": b},
                    },
                }
            ],
            "paragraphStyleRange": [
                {
                    "_obj": "paragraphStyleRange",
                    "from": 0,
                    "to": n,
                    "paragraphStyle": {
                        "_obj": "paragraphStyle",
                        "align": {"_enum": "alignmentType", "_value": "center"},
                    },
                }
            ],
        },
    }


def _set_fill_opacity(value: float) -> Dict[str, Any]:
    return {
        "_obj": "set",
        "_target": _target_current(),
        "to": {"_obj": "layer", "fillOpacity": {"_unit": "percentUnit", "_value": value}},
    }


def _add_white_stroke(size_px: int = 8) -> Dict[str, Any]:
    return {
        "_obj": "set",
        "_target": [
            {"_property": "layerEffects", "_ref": "property"},
            {"_enum": "ordinal", "_ref": "layer", "_value": "targetEnum"},
        ],
        "to": {
            "_obj": "layerEffects",
            "frameFX": {
                "_obj": "frameFX",
                "enabled": True,
                "present": True,
                "showInDialog": True,
                "style": {"_enum": "frameStyle", "_value": "outsetFrame"},
                "size": {"_unit": "pixelsUnit", "_value": size_px},
                "mode": {"_enum": "blendMode", "_value": "normal"},
                "opacity": {"_unit": "percentUnit", "_value": 100},
                "paintType": {"_enum": "frameFill", "_value": "solidColor"},
                "color": {"_obj": "RGBColor", "red": 255.0, "grain": 255.0, "blue": 255.0},
                "overprint": False,
            },
            "scale": {"_unit": "percentUnit", "_value": 100},
        },
    }


def build_text_embed_actions(
    text: str,
    font: str = "Impact",
    size_px: int = 320,
    color_rgb: tuple = (255.0, 255.0, 255.0),
    stroke_px: int = 8,
) -> List[Dict[str, Any]]:
    """
    Build the two-layer "text behind subject" wrap with the user's ``text``.

    Layer order (bottom→top): background, SOLID text, subject copy, OUTLINE text.
    """
    text = (text or "").strip() or "TEXT"

    return [
        # Isolate the subject onto its own layer.
        {"_obj": "autoCutout", "sampleAllLayers": False},
        {"_obj": "copyToLayer"},  # subject copy → top, active

        # 1) SOLID text BEHIND the subject: insert above the background.
        _select_ordinal("back"),
        _make_text_layer(text, font, size_px, color_rgb),

        # 2) OUTLINE text ON TOP of the subject: insert above the subject copy,
        #    then fill 0% + white stroke so only the outline shows over the subject.
        _select_ordinal("front"),
        _make_text_layer(text, font, size_px, color_rgb),
        _set_fill_opacity(0.0),
        _add_white_stroke(stroke_px),
    ]
