# Deselect (Clear Selection)

**Action:** `set`  
**Target:** `channel` (selection property)  
**Menu Location:** Select > Deselect (Ctrl/Cmd + D)

Clears the current selection, removing the "marching ants" selection border. This is commonly needed after creating a mask from a selection.

## Common Workflow

**Typical use case:** After creating a layer mask from a selection, deselect to remove the marching ants and continue editing.

**Sequence:**
1. `autoCutout` - Select subject
2. `make` (mask) - Create mask from selection
3. `set` (this action) - **Deselect to clear marching ants**

## JSON Structure

```json
{
    "_obj": "set",
    "_target": [
        {
            "_ref": "channel",
            "_property": "selection"
        }
    ],
    "to": {
        "_enum": "ordinal",
        "_value": "none"
    }
}
```

## Parameters

- `_target`: Specifies we're modifying the selection
    - `_ref`: `"channel"`
    - `_property`: `"selection"`
- `to`: The new selection state
    - `_enum`: `"ordinal"`
    - `_value`: `"none"` - Clears the selection

## Related Actions

| Sequence | Action | Purpose |
|----------|--------|---------|
| Before | `autoCutout` | Select Subject |
| Before | `colorRange` | Select by color |
| Before | `make` (mask) | Create mask from selection |
| **This** | `set` (deselect) | Clear selection |

## Notes

- Always deselect after creating a mask to remove the marching ants visual
- This action has no effect if there is no active selection
- Deselecting does NOT affect any masks that were created from the selection

