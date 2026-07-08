# Unsharp Mask

**Action:** `unsharpMask`
**Target:** None (implicitly targets active layer)

Sharpening filter used to correct blurring in the scanned image or original.

## JSON Structure

```json
{
    "_obj": "unsharpMask",
    "amount": {
        "_unit": "percentUnit",
        "_value": 500.0
    },
    "radius": {
        "_unit": "pixelsUnit",
        "_value": 0.6
    },
    "threshold": 0
}
```

## Parameters

- `amount`: (Unit) The strength of the sharpening (percent).
    - `_unit`: "percentUnit"
    - `_value`: Numeric value (usually 1-500).
- `radius`: (Unit) The radius of the sharpening effect.
    - `_unit`: "pixelsUnit"
    - `_value`: Numeric value (pixels).
- `threshold`: (Integer) The threshold level (0-255). Determines how different pixels must be from surrounding area to be sharpened.

