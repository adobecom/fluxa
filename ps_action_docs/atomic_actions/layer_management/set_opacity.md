# Set Layer Opacity

**Action:** `set`  
**Target:** `layer` (current)

Adjusts the opacity of the currently selected layer.

## JSON Structure

```json
{
    "_obj": "set",
    "_target": [
        {
            "_enum": "ordinal",
            "_ref": "layer",
            "_value": "targetEnum"
        }
    ],
    "to": {
        "_obj": "layer",
        "opacity": {
            "_unit": "percentUnit",
            "_value": 70.0
        }
    }
}
```

## Parameters

- `to.opacity._value`: Float value (0.0 - 100.0) representing opacity percentage.

