# Add Noise

**Action:** `addNoise`
**Target:** None (implicitly targets active layer)

Adds random pixels to the image to simulate film grain or texture.

## JSON Structure

```json
{
    "_obj": "addNoise",
    "distort": {
        "_enum": "distort",
        "_value": "gaussianDistribution"
    },
    "monochromatic": true,
    "noise": {
        "_unit": "percentUnit",
        "_value": 2.96
    }
}
```

## Parameters

- `distort`: (Enum) Distribution type.
    - `gaussianDistribution`: Speckled look.
    - `uniformDistribution`: More absolute random appearance.
- `monochromatic`: (Boolean) If `true`, applies noise using only neutral tones (black/white/gray). If `false`, applies color noise.
- `noise`: (Unit) The amount of noise (0-100% usually).
    - `_unit`: "percentUnit"
    - `_value`: Numeric value (e.g., 2.96)

