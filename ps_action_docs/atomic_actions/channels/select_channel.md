# Select Channel

**Action:** `select`  
**Target:** `channel`

Selects a specific color channel in the Channels panel (often used to reset selection to RGB after channel manipulation).

## JSON Structure

```json
{
    "_obj": "select",
    "_target": [
        {
            "_enum": "channel",
            "_ref": "channel",
            "_value": "RGB"
        }
    ],
    "makeVisible": false
}
```

## Parameters

- `_target._value`: The channel name (`RGB`, `Red`, `Green`, `Blue`, or `mask`).

