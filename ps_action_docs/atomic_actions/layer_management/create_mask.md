# Create Layer Mask

**Action:** `make`  
**Target:** `channel` (relative to layer)

Creates a layer mask on the currently selected layer.

## JSON Structure

```json
{
    "_obj": "make",
    "at": {
        "_enum": "channel",
        "_ref": "channel",
        "_value": "mask"
    },
    "new": {
        "_class": "channel"
    },
    "using": {
        "_enum": "userMaskEnabled",
        "_value": "revealAll"
    }
}
```

## Parameters

- `at`: Specifies where to create the new object.
    - `_value`: `mask` indicates this is a layer mask.
- `new`: The type of object being created (`channel`).
- `using`: The initial state of the mask.
    - `_value`: 
        - `revealAll`: White mask (shows everything).
        - `hideAll`: Black mask (hides everything).

