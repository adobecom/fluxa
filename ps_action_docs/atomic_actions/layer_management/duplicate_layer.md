# Duplicate Layer

**Action:** `duplicate`
**Target:** `layer`

Duplicates the specified layer.

## JSON Structure

```json
{
    "_obj": "duplicate",
    "_target": [
        {
            "_enum": "ordinal",
            "_ref": "layer",
            "_value": "targetEnum"
        }
    ],
    "name": "Rain 2",
    "version": 5
}
```

## Parameters

- `name`: (String) Name for the duplicated layer.
- `version`: (Integer) Internal version number (usually 5).
- `_target`: Target layer to duplicate.

