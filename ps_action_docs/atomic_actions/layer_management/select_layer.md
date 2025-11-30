# Select Layer

**Action:** `select`  
**Target:** `layer`

Selects a specific layer by ID, name, or relative position.

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
