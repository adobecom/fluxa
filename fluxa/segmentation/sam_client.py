"""
Object segmentation (SAM-2 + Florence-2), self-contained in fluxa-re.

Given an image and a text prompt (the object to select), Florence-2 detects the
object(s) and SAM-2 segments them into a binary mask; the object is then cut out
onto a transparent PNG for compositing.

Models are loaded lazily and cached for the process lifetime (first call pays the
load/download cost). If the ML stack isn't installed or inference fails, a
SegmentationError is raised so callers can fall back to autoCutout — nothing breaks.

Config via env vars:
  SAM_CHECKPOINT / SAM_CONFIG  - see sam.py
  FLORENCE_CHECKPOINT          - HF id (default microsoft/Florence-2-base)
"""

from __future__ import annotations

import logging
import os
import tempfile
from typing import Any, Optional

logger = logging.getLogger(__name__)


class SegmentationError(RuntimeError):
    """Raised when we cannot produce an object mask (caller may fall back)."""


# Cached, lazily-initialized model handles.
_MODELS: dict[str, Any] = {}


def _get_devices():
    """Florence on MPS (Mac) when available; SAM on CPU (matches the tested setup)."""
    import torch

    florence_device = torch.device("mps") if torch.backends.mps.is_available() else torch.device("cpu")
    sam_device = torch.device("cpu")
    return florence_device, sam_device


def _load_models():
    """Load + cache Florence and SAM models. Raises SegmentationError on failure."""
    if _MODELS:
        return _MODELS
    try:
        from .florence import load_florence_model
        from .sam import load_sam_image_model

        florence_device, sam_device = _get_devices()
        logger.info("[seg] Loading Florence-2 + SAM-2 (first call; may download weights)...")
        fl_model, fl_processor = load_florence_model(device=florence_device)
        sam_model = load_sam_image_model(device=sam_device)
        _MODELS.update(
            florence_model=fl_model,
            florence_processor=fl_processor,
            florence_device=florence_device,
            sam_model=sam_model,
        )
        logger.info("[seg] Models loaded.")
        return _MODELS
    except Exception as e:
        raise SegmentationError(
            f"could not load SAM/Florence models ({e}); is the ML stack installed? "
            "(pip install -r requirements.txt)"
        ) from e


def get_object_mask(image_path: str, object_text: str, out_dir: Optional[str] = None) -> str:
    """
    Produce a white-on-black binary mask of ``object_text`` in the image.

    Runs Florence-2 open-vocabulary detection → SAM-2 segmentation in-process.
    Supports comma-separated objects (e.g. "person, surfboard"). Raises
    SegmentationError on any failure.
    """
    try:
        import numpy as np
        import supervision as sv
        from PIL import Image

        from .florence import run_florence_inference, FLORENCE_OPEN_VOCABULARY_DETECTION_TASK
        from .sam import run_sam_inference
    except Exception as e:
        raise SegmentationError(f"segmentation deps missing ({e})") from e

    models = _load_models()
    fl_model = models["florence_model"]
    fl_processor = models["florence_processor"]
    fl_device = models["florence_device"]
    sam_model = models["sam_model"]

    image = Image.open(image_path).convert("RGB")

    try:
        detections_list = []
        for text in [t.strip() for t in object_text.split(",") if t.strip()]:
            _, result = run_florence_inference(
                model=fl_model,
                processor=fl_processor,
                device=fl_device,
                image=image,
                task=FLORENCE_OPEN_VOCABULARY_DETECTION_TASK,
                text=text,
            )
            detections = sv.Detections.from_lmm(
                lmm=sv.LMM.FLORENCE_2, result=result, resolution_wh=image.size
            )
            detections = run_sam_inference(sam_model, image, detections)
            detections_list.append(detections)

        if not detections_list:
            raise SegmentationError(f"no objects parsed from {object_text!r}")

        detections = sv.Detections.merge(detections_list)
        detections = run_sam_inference(sam_model, image, detections)

        if detections.mask is None or len(detections.mask) == 0:
            raise SegmentationError(f"no mask produced for {object_text!r}")

        # Union all detection masks into one binary mask.
        mask_array = np.zeros((image.height, image.width), dtype=np.uint8)
        for m in detections.mask:
            mask_array = np.maximum(mask_array, m.astype(np.uint8))

        out_dir = out_dir or tempfile.mkdtemp(prefix="fluxa_seg_")
        os.makedirs(out_dir, exist_ok=True)
        mask_path = os.path.join(out_dir, "object_mask.png")
        Image.fromarray(mask_array * 255, mode="L").save(mask_path)
        logger.info(f"[seg] Mask for {object_text!r} written to {mask_path}")
        return mask_path
    except SegmentationError:
        raise
    except Exception as e:
        raise SegmentationError(f"segmentation failed for {object_text!r}: {e}") from e


def cutout_object(image_path: str, mask_path: str, out_path: Optional[str] = None) -> str:
    """Cut the masked object onto a transparent RGBA PNG (mask → alpha channel)."""
    from PIL import Image

    img = Image.open(image_path).convert("RGBA")
    mask = Image.open(mask_path).convert("L")
    if mask.size != img.size:
        mask = mask.resize(img.size, Image.LANCZOS)
    img.putalpha(mask)

    out_path = out_path or os.path.join(os.path.dirname(mask_path) or ".", "object_cutout.png")
    img.save(out_path)
    logger.info(f"[seg] Object cutout written to {out_path}")
    return out_path


def segment_and_cutout(image_path: str, object_text: str, out_dir: Optional[str] = None) -> str:
    """Mask the named object, then return a transparent-PNG cutout path."""
    out_dir = out_dir or tempfile.mkdtemp(prefix="fluxa_seg_")
    mask_path = get_object_mask(image_path, object_text, out_dir=out_dir)
    return cutout_object(image_path, mask_path, out_path=os.path.join(out_dir, "object_cutout.png"))
