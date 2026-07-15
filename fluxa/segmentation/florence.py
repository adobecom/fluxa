"""
Florence-2 loading + inference (self-contained in fluxa-re).

Ported so fluxa does not depend on the artify project. Florence-2 does
open-vocabulary object detection from a text prompt; the resulting boxes feed
SAM-2 for segmentation.
"""

from __future__ import annotations

import os
from typing import Any, Dict, Tuple, Union
from unittest.mock import patch

FLORENCE_CHECKPOINT = "microsoft/Florence-2-base"
FLORENCE_OPEN_VOCABULARY_DETECTION_TASK = "<OPEN_VOCABULARY_DETECTION>"


def _fixed_get_imports(filename: Union[str, os.PathLike]) -> list:
    """Work around Florence-2 hard-importing flash_attn (not needed on CPU/MPS)."""
    from transformers.dynamic_module_utils import get_imports

    if not str(filename).endswith("/modeling_florence2.py"):
        return get_imports(filename)
    imports = get_imports(filename)
    if "flash_attn" in imports:
        imports.remove("flash_attn")
    return imports


def load_florence_model(device, checkpoint: str = FLORENCE_CHECKPOINT) -> Tuple[Any, Any]:
    """Load the Florence-2 model + processor onto ``device``."""
    from transformers import AutoModelForCausalLM, AutoProcessor

    with patch("transformers.dynamic_module_utils.get_imports", _fixed_get_imports):
        model = (
            AutoModelForCausalLM.from_pretrained(checkpoint, trust_remote_code=True)
            .to(device)
            .eval()
        )
        processor = AutoProcessor.from_pretrained(checkpoint, trust_remote_code=True)
        return model, processor


def run_florence_inference(model, processor, device, image, task: str, text: str = "") -> Tuple[str, Dict]:
    """Run a Florence-2 task (e.g. open-vocabulary detection) on ``image``."""
    prompt = task + text
    inputs = processor(text=prompt, images=image, return_tensors="pt").to(device)
    generated_ids = model.generate(
        input_ids=inputs["input_ids"],
        pixel_values=inputs["pixel_values"],
        max_new_tokens=1024,
        num_beams=3,
    )
    generated_text = processor.batch_decode(generated_ids, skip_special_tokens=False)[0]
    response = processor.post_process_generation(generated_text, task=task, image_size=image.size)
    return generated_text, response
