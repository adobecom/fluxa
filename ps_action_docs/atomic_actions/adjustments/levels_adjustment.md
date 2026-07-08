# Levels Adjustment

**Action:** `levels`
**Target:** None (implicitly targets active layer)

Applies a Levels adjustment to the active layer (destructive). Can adjust gamma, input, and output levels for composite or specific channels.

## JSON Structure

```json
{
    "_obj": "levels",
    "adjustment": [
        {
            "_obj": "levelsAdjustment",
            "channel": {
                "_enum": "channel",
                "_ref": "channel",
                "_value": "composite"
            },
            "gamma": 1.22,
            "input": [
                0,
                255
            ],
            "output": [
                0,
                255
            ]
        }
    ],
    "presetKind": {
        "_enum": "presetKindType",
        "_value": "presetKindCustom"
    }
}
```

## Parameters

- `adjustment`: Array containing the adjustment settings.
- `channel`: The channel to target (e.g., `composite`, `red`, `green`, `blue`).
    - `_value`: `composite` (default), `red`, `green`, `blue`, or channel ID.
- `gamma`: (Float) The midtone (gamma) value.
- `input`: (Array of 2 integers) [shadow, highlight] input levels (0-255). Maps dark and light values.
- `output`: (Array of 2 integers) [shadow, highlight] output levels (0-255). Maps output intensity.
