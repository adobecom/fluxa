# Select Layer

**Action:** `select`  
**Target:** `layer`

Selects a specific layer by ID, name, or relative position.

## ⚠️ Important: When NOT to Use Select

**After `placeEvent`:** The placed layer is **automatically selected**. Do NOT add a `select` action after `placeEvent` - it's unnecessary and may cause issues.

**Edge case warning:** 
- `forwardEnum` selects the layer ABOVE the current layer. If the current layer is already the **topmost layer**, this may select an unexpected layer or fail.
- `backEnum` selects the layer BELOW the current layer. If the current layer is already the **bottom layer**, this may select an unexpected layer or fail.

**Only use relative selection (`forwardEnum`/`backEnum`) when you are certain there is a layer in that direction.**

## Select by Relative Position (Forward/Backward)

```json
{
    "_obj": "select",
    "_target": [
        {
            "_enum": "ordinal",
            "_ref": "layer",
            "_value": "forwardEnum" 
        }
    ],
    "makeVisible": false
}
```

> Note: `_value` can be `forwardEnum`, `backwardEnum`, or `targetEnum`.

## Select by Name

Selects a specific layer by its name.

```json
{
    "_obj": "select",
    "_target": [
        {
            "_ref": "layer",
            "_name": "Rain 1"
        }
    ],
    "makeVisible": false,
    "selectionModifier": {
        "_enum": "selectionModifierType",
        "_value": "addToSelectionContinuous"
    }
}
```

## Parameters

- `_target`: Specifies which layer to select.
    - `_name`: Name of the layer to select.
    - `_enum`: `ordinal` for relative selection.
    - `_value`: `forwardEnum` (layer above), `backwardEnum` (layer below).
- `makeVisible`: (Boolean) Whether to toggle visibility upon selection.
- `selectionModifier`: (Optional) Modifies how the selection is applied.
    - `_value`:
        - `addToSelection`: Adds to current selection.
        - `addToSelectionContinuous`: Adds to selection (often used for multi-select).
        - `removeFromSelection`: Removes from selection.

## Notes

- **After `placeEvent`**: The placed layer is already selected. Do NOT use `select` immediately after `placeEvent`.
- **After `duplicate`**: The duplicated layer is usually selected automatically.
- **After `make` (new layer)**: The new layer is usually selected automatically.
- Use `forwardEnum`/`backEnum` only when navigating between existing layers, not after creating/placing new layers.
