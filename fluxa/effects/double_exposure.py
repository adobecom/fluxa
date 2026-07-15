"""
Double exposure — deterministic ActionJSON builder.

The classic effect: a second (texture) image shows *inside* the subject's
silhouette, screen-blended. Steps: isolate the subject → place the second image
on top → clip it to the subject (create clipping mask) → set Screen blend.
Render-tested against the v1 `actionJSON` endpoint (produces the texture-inside-
silhouette look).

This is a TWO-image effect: inputs[0] is the subject photo, additionalImages[0]
is the texture/second image.

Why deterministic instead of the agent: the tutorial's manual brush-on-mask +
eyedropper solid-color-fill + merge-visible steps make the LLM emit inconsistent
output (a solid-color wipe → black frame, or the two images stacked unclipped).
The clip + Screen recipe reproduces the effect reliably with no manual steps.
"""

from __future__ import annotations

from typing import Any, Dict, List


def _target_current() -> List[Dict[str, Any]]:
    return [{"_enum": "ordinal", "_ref": "layer", "_value": "targetEnum"}]


def build_double_exposure_actions(
    additional_image_index: int = 0,
    blend_mode: str = "screen",
    opacity: float = 58.0,
) -> List[Dict[str, Any]]:
    """
    Build double-exposure ActionJSON.

    autoCutout (subject) → copyToLayer → placeEvent(second image) →
    groupEvent (clip the second image to the subject) → Screen blend → opacity.
    """
    return [
        {"_obj": "autoCutout", "sampleAllLayers": False},
        {"_obj": "copyToLayer"},  # subject copy → top, active
        {
            "_obj": "placeEvent",
            "null": {"_kind": "local", "_path": f"ACTION_JSON_OPTIONS_ADDITIONAL_IMAGES_{additional_image_index}"},
            "freeTransformCenterState": {"_enum": "quadCenterState", "_value": "QCSAverage"},
            "offset": {
                "_obj": "offset",
                "horizontal": {"_unit": "pixelsUnit", "_value": 0},
                "vertical": {"_unit": "pixelsUnit", "_value": 0},
            },
        },
        # Clip the placed texture to the subject copy directly below → the texture
        # only shows within the subject silhouette.
        {"_obj": "groupEvent", "_target": _target_current()},
        # Screen blend drops the dark pixels so the texture reads as a blend.
        {
            "_obj": "set",
            "_target": _target_current(),
            "to": {"_obj": "layer", "mode": {"_enum": "blendMode", "_value": blend_mode}},
        },
        # Slightly reduced opacity lets the subject's own features show through.
        {
            "_obj": "set",
            "_target": _target_current(),
            "to": {"_obj": "layer", "opacity": {"_unit": "percentUnit", "_value": float(opacity)}},
        },
    ]
