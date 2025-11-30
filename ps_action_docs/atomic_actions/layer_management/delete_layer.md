# Delete Layer

**Action:** `delete`
**Target:** `layer`

Deletes the specified layer.

## JSON Structure

```json
{
    "_obj": "delete",
    "_target": [
        {
            "_enum": "ordinal",
            "_ref": "layer",
            "_value": "hidden"
        }
    ]
}
```

## Parameters

- `_target`: Target layer to delete.
    - `_value`: `hidden` (delete hidden layers), `targetEnum` (delete active layer).

