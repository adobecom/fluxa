"""Object segmentation for the glow / highlight pipeline.

Self-contained SAM-2 + Florence-2: gets a binary mask for a user-named object and
cuts it out onto a transparent layer for compositing. Models run in-process
(loaded lazily) — no dependency on the artify project.
"""

from .sam_client import get_object_mask, cutout_object, segment_and_cutout, SegmentationError

__all__ = ["get_object_mask", "cutout_object", "segment_and_cutout", "SegmentationError"]
