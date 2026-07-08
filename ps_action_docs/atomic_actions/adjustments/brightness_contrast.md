# Brightness/Contrast

**Action:** `brightnessEvent`
**Target:** None (implicitly targets active layer)

Applies a Brightness/Contrast adjustment to the active layer (destructive).

## JSON Structure

```json
{
    "_obj": "brightnessEvent",
    "brightness": -11,
    "center": 15,
    "useLegacy": false
}
```

## Parameters

- `brightness`: (Integer) The brightness value (e.g., -150 to 150).
- `center`: (Integer) The contrast value (e.g., -50 to 100). Note: Key is named `center` in the JSON.
- `useLegacy`: (Boolean) Whether to use the legacy algorithm (usually `false`).

