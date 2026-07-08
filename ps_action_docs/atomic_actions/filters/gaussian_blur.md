# Gaussian Blur

**Action:** `gaussianBlur`
**Target:** None (implicitly targets active layer)

Applies a Gaussian blur to the active layer or selection, softening the image.

## JSON Structure

```json
{
    "_obj": "gaussianBlur",
    "radius": {
        "_unit": "pixelsUnit",
        "_value": 63.5
    }
}
```

## Parameters

- `radius`: (Unit) The radius of the blur.
    - `_unit`: "pixelsUnit"
    - `_value`: Numeric value (pixels).

