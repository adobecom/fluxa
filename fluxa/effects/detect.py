"""
Unified effect classifier.

One LLM call decides whether a tutorial's PRIMARY effect is one of the
deterministic effects we build in code (glow, background blur, …) or "none"
(fall through to the normal agent). Extend `_EFFECTS` + the prompt to add more.
"""

from __future__ import annotations

import json
import logging
from typing import Any, Dict

logger = logging.getLogger(__name__)

# Effects we can build deterministically. "none" → use the normal agent flow.
_EFFECTS = ["glow", "background_blur", "text_embed", "double_exposure", "none"]

_CLASSIFY_PROMPT = (
    "You classify Photoshop tutorials by their PRIMARY effect. Choose exactly one:\n"
    "- \"glow\": making a specific object glow / adding a glow or light effect to an object.\n"
    "- \"background_blur\": portrait / bokeh / depth-of-field — keep the subject sharp and "
    "blur the background behind it.\n"
    "- \"text_embed\": placing TEXT behind the subject (text-behind-subject / text-masking "
    "effect where the person or object partly covers a big word).\n"
    "- \"double_exposure\": blending a SECOND image inside the subject's silhouette "
    "(clip a texture/landscape into the person and blend).\n"
    "- \"none\": anything else.\n"
    "Only pick a specific effect if it is the MAIN point of the tutorial.\n"
    'Reply ONLY JSON: {"effect": "glow"|"background_blur"|"text_embed"|"double_exposure"|"none", '
    '"object": "<for glow: the object that should glow; for background_blur: the subject to '
    'keep sharp; otherwise null>"}.'
)


def classify_effect(transcript: str, api_key: str, model: str = "gpt-5.1",
                    max_chars: int = 6000) -> Dict[str, Any]:
    """
    Return {"effect": <one of _EFFECTS>, "object": Optional[str]}.

    On any error returns effect="none" so the normal pipeline proceeds unchanged.
    """
    try:
        from openai import OpenAI

        client = OpenAI(api_key=api_key)
        resp = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": _CLASSIFY_PROMPT},
                {"role": "user", "content": transcript[:max_chars]},
            ],
            response_format={"type": "json_object"},
        )
        data = json.loads(resp.choices[0].message.content or "{}")
        effect = str(data.get("effect", "none"))
        if effect not in _EFFECTS:
            effect = "none"
        obj = data.get("object")
        if isinstance(obj, str) and obj.strip().lower() in ("null", "none", ""):
            obj = None
        return {"effect": effect, "object": obj}
    except Exception as e:  # never break the pipeline
        logger.warning(f"[detect] effect classification failed ({e}); treating as none")
        return {"effect": "none", "object": None}
