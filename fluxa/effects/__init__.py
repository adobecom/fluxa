"""Deterministic, code-generated Photoshop effects (not LLM-authored).

These build ActionJSON for well-defined effects whose reliability we don't want
to leave to the model. The LLM's job is only to *detect* the effect and extract
parameters; the exact action sequence is produced here and has been render-tested
against the Adobe actionJSON endpoint.
"""

from .glow import build_glow_actions, build_glow_actions_for_cutout, GlowParams, detect_glow_effect
from .background_blur import build_background_blur_actions
from .text_embed import build_text_embed_actions
from .double_exposure import build_double_exposure_actions
from .detect import classify_effect

__all__ = [
    "build_glow_actions",
    "build_glow_actions_for_cutout",
    "GlowParams",
    "detect_glow_effect",
    "build_background_blur_actions",
    "build_text_embed_actions",
    "build_double_exposure_actions",
    "classify_effect",
]
