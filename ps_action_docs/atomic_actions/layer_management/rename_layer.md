# Rename Layer

**Action:** `set`  
**Target:** `layer` (current)

Renames the currently selected layer.

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
        "name": "New Layer Name"
    }
}
```

## Parameters

- `to.name`: The new string name for the layer.

