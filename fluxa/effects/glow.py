"""
Glow effect — deterministic ActionJSON builder.

Reproduces the classic "make an object glow" tutorial move:
isolate the object → duplicate it → set the copy to **Linear Dodge (Add)** →
apply increasingly large **Gaussian Blur** on stacked duplicates → soft radiant
halo. Optionally darken the background first so the glow reads.

This sequence was render-tested against the Adobe v1 `actionJSON` endpoint (the
one that still has quota), so it does not depend on `smartObject` / neural /
v2 endpoints.

IMPORTANT — why isolation matters: Linear Dodge is *additive*. Glowing the whole
frame blows it out to white. The glow must come from an isolated object, which is
why the pipeline segments the user-chosen object (SAM/Florence) or falls back to
`autoCutout` before calling this builder.
"""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

# Blend-mode token verified against the Photoshop source (enumPsLinearDodge).
_LINEAR_DODGE = "linearDodge"


_GLOW_DETECT_PROMPT = (
    "You classify Photoshop tutorials. Decide if the tutorial's PRIMARY effect is "
    "making a specific object GLOW or adding a glow/light/light-source effect to an "
    "object (e.g. a glowing peanut, neon sign, glowing orb, light rays from an object). "
    "It is NOT a glow tutorial if glow is only a minor incidental step. "
    'Reply ONLY JSON: {"is_glow": true|false, "object": "<the object that should glow, '
    'or null if unclear>"}.'
)


def detect_glow_effect(transcript: str, api_key: str, model: str = "gpt-5.1",
                       max_chars: int = 6000) -> Dict[str, Any]:
    """
    Classify whether this transcript is a glow tutorial, and guess the glowing object.

    Returns {"is_glow": bool, "object": Optional[str]}. On any error, returns
    is_glow=False so the normal pipeline proceeds unchanged.
    """
    try:
        from openai import OpenAI

        client = OpenAI(api_key=api_key)
        resp = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": _GLOW_DETECT_PROMPT},
                {"role": "user", "content": transcript[:max_chars]},
            ],
            response_format={"type": "json_object"},
        )
        data = json.loads(resp.choices[0].message.content or "{}")
        obj = data.get("object")
        if isinstance(obj, str) and obj.strip().lower() in ("null", "none", ""):
            obj = None
        return {"is_glow": bool(data.get("is_glow")), "object": obj}
    except Exception as e:  # never let detection break the pipeline
        logger.warning(f"[glow] detection failed ({e}); treating as non-glow")
        return {"is_glow": False, "object": None}


def _target_current() -> List[Dict[str, Any]]:
    return [{"_enum": "ordinal", "_ref": "layer", "_value": "targetEnum"}]


@dataclass
class GlowParams:
    """Tunable glow parameters (sensible defaults from the render-tested recipe)."""

    # Radii for each stacked glow layer, small→large (soft, layered bloom).
    blur_radii: List[float] = field(default_factory=lambda: [20.0, 90.0, 250.0])
    # Opacity of the first (tightest) glow layer; wider layers inherit via duplicate.
    first_layer_opacity: float = 70.0
    # How much to darken the background so the glow stands out (0 = don't darken).
    darken_background: float = 0.0
    # If True, isolate the subject with autoCutout first (used when no external
    # cutout/mask is supplied). If False, the caller has already placed the glow
    # source as the current top layer (e.g. a SAM/Florence cutout).
    isolate_with_autocutout: bool = True


def build_glow_actions(params: Optional[GlowParams] = None) -> List[Dict[str, Any]]:
    """
    Build the glow ActionJSON.

    Preconditions on document state:
      - If ``isolate_with_autocutout`` is True: the base image is loaded; this
        builder runs autoCutout + copyToLayer to put the subject on its own layer.
      - If False: the object to glow is already the current top layer (e.g. a
        placed SAM/Florence cutout on a transparent background).

    Returns a list of action dicts, ready to send to the actionJSON endpoint.
    """
    p = params or GlowParams()
    if not p.blur_radii:
        raise ValueError("blur_radii must contain at least one radius")

    actions: List[Dict[str, Any]] = []

    # 1) Isolate the glow source onto its own layer.
    if p.isolate_with_autocutout:
        actions.append({"_obj": "autoCutout", "sampleAllLayers": False})
        actions.append({"_obj": "copyToLayer"})  # bright subject copy → top, active

        # Darken the ORIGINAL background layer, then return to the subject copy.
        if p.darken_background and p.darken_background > 0:
            actions.append(_select_ordinal("back"))       # original image (bottom)
            actions.extend(_darken_active(p.darken_background))
            actions.append(_select_ordinal("front"))      # back to the bright subject copy

    # 2) Glow the currently-active layer (the isolated subject / placed cutout).
    actions.extend(_glow_core(p))
    return actions


def _select_ordinal(value: str) -> Dict[str, Any]:
    return {"_obj": "select", "_target": [{"_enum": "ordinal", "_ref": "layer", "_value": value}]}


def _darken_active(amount: float) -> List[Dict[str, Any]]:
    """Darken the active layer (used on the background so the glowing object pops)."""
    return [
        {
            "_obj": "brightnessEvent",
            "brightness": -int(min(150, max(0, amount))),
            "contrast": 0,
            "useLegacy": False,
        }
    ]


def _glow_core(p: GlowParams) -> List[Dict[str, Any]]:
    """The glow itself, applied to whatever layer is currently active.

    duplicate → Linear Dodge → smallest blur → opacity, then successive
    duplicates with larger blur radii for soft, layered falloff.
    """
    actions: List[Dict[str, Any]] = []
    actions.append({"_obj": "duplicate", "_target": _target_current()})
    actions.append(
        {
            "_obj": "set",
            "_target": _target_current(),
            "to": {"_obj": "layer", "mode": {"_enum": "blendMode", "_value": _LINEAR_DODGE}},
        }
    )
    actions.append(
        {"_obj": "gaussianBlur", "radius": {"_unit": "pixelsUnit", "_value": float(p.blur_radii[0])}}
    )
    actions.append(
        {
            "_obj": "set",
            "_target": _target_current(),
            "to": {"_obj": "layer", "opacity": {"_unit": "percentUnit", "_value": float(p.first_layer_opacity)}},
        }
    )
    for radius in p.blur_radii[1:]:
        actions.append({"_obj": "duplicate", "_target": _target_current()})
        actions.append(
            {"_obj": "gaussianBlur", "radius": {"_unit": "pixelsUnit", "_value": float(radius)}}
        )
    return actions


def _place_additional_image(index: int = 0) -> Dict[str, Any]:
    """placeEvent that places additionalImages[index] as a new (current) layer."""
    return {
        "_obj": "placeEvent",
        "null": {"_kind": "local", "_path": f"ACTION_JSON_OPTIONS_ADDITIONAL_IMAGES_{index}"},
        "freeTransformCenterState": {"_enum": "quadCenterState", "_value": "QCSAverage"},
        "offset": {
            "_obj": "offset",
            "horizontal": {"_unit": "pixelsUnit", "_value": 0},
            "vertical": {"_unit": "pixelsUnit", "_value": 0},
        },
    }


def build_glow_actions_for_cutout(params: Optional[GlowParams] = None,
                                  additional_image_index: int = 0) -> List[Dict[str, Any]]:
    """
    Glow using an externally-provided object cutout (e.g. a SAM/Florence result).

    The base document is the original image; the transparent-PNG cutout of the
    object-to-glow is supplied as additionalImages[index]. This places the cutout
    on top (becoming the current layer), then runs the glow on it — so the glow
    comes only from the chosen object, exactly as isolation requires.
    """
    p = params or GlowParams()
    actions: List[Dict[str, Any]] = []

    # 1) Darken the base image (the only/active layer) FIRST, so the subject
    #    behind the glowing object is darkened. Doing it before placing the cutout
    #    avoids any layer-reselect ambiguity.
    if p.darken_background and p.darken_background > 0:
        actions.extend(_darken_active(p.darken_background))

    # 2) Place the object cutout on top (it becomes the active layer) and glow it.
    #    The glow now comes ONLY from the cutout, over the darkened base.
    actions.append(_place_additional_image(additional_image_index))
    actions.extend(_glow_core(p))
    return actions
