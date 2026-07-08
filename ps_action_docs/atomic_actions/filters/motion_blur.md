# Motion Blur

**Action:** `motionBlur`
**Target:** None (implicitly targets active layer)

Applies a blur in a specific direction (angle) to simulate motion.

## JSON Structure

```json
{
    "descriptor": {
        "_obj": "motionBlur",
        "angle": 70,
        "distance": {
            "_unit": "pixelsUnit",
            "_value": 58.0
        }
    },
    "options": {
        "dialogOptions": "display"
    }
}
```

## Parameters

- `angle`: (Integer) The angle of the motion blur (0-360).
- `distance`: (Unit) The length of the blur.
    - `_unit`: "pixelsUnit"
    - `_value`: Numeric value (pixels).
- `options`: (Optional) Dialog display options.

