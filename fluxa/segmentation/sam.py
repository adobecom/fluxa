"""
SAM-2 loading + inference (self-contained in fluxa-re).

Ported so fluxa does not depend on the artify project. Given detection boxes
(from Florence-2), SAM-2 produces precise segmentation masks.

The checkpoint path and config are configurable via env vars:
  SAM_CHECKPOINT - path to sam2_hiera_small.pt (auto-downloaded if missing)
  SAM_CONFIG     - SAM-2 config name (default: sam2_hiera_s.yaml, from the sam2 pkg)
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent.parent  # fluxa-re/
_DEFAULT_CHECKPOINT = str(REPO_ROOT / "checkpoints" / "sam2_hiera_small.pt")
_CHECKPOINT_URL = "https://dl.fbaipublicfiles.com/segment_anything_2/072824/sam2_hiera_small.pt"
_DEFAULT_CONFIG = "sam2_hiera_s.yaml"


def _checkpoint_path() -> str:
    return os.getenv("SAM_CHECKPOINT", _DEFAULT_CHECKPOINT)


def _config_name() -> str:
    return os.getenv("SAM_CONFIG", _DEFAULT_CONFIG)


def download_checkpoint_if_needed(checkpoint_path: str, url: str = _CHECKPOINT_URL) -> None:
    """Download the SAM-2 checkpoint if it isn't already on disk."""
    if os.path.exists(checkpoint_path):
        return
    import requests

    os.makedirs(os.path.dirname(checkpoint_path), exist_ok=True)
    print(f"[sam] Downloading checkpoint to {checkpoint_path} ...")
    resp = requests.get(url)
    resp.raise_for_status()
    with open(checkpoint_path, "wb") as f:
        f.write(resp.content)
    print("[sam] Download complete.")


def load_sam_image_model(device, config: str = None, checkpoint: str = None):
    """Build SAM-2 and return an image predictor."""
    from sam2.build_sam import build_sam2
    from sam2.sam2_image_predictor import SAM2ImagePredictor

    config = config or _config_name()
    checkpoint = checkpoint or _checkpoint_path()
    download_checkpoint_if_needed(checkpoint)
    model = build_sam2(config, checkpoint, device=device)
    return SAM2ImagePredictor(sam_model=model)


def run_sam_inference(model: Any, image, detections):
    """Segment the detected boxes; attach boolean masks to ``detections``."""
    import numpy as np

    arr = np.array(image.convert("RGB"))
    model.set_image(arr)
    mask, _score, _ = model.predict(box=detections.xyxy, multimask_output=False)

    # Normalize shape (N,1,H,W) or (H,W) → (N,H,W) boolean.
    if len(mask.shape) == 4:
        mask = np.squeeze(mask)
    detections.mask = mask.astype(bool)
    return detections
