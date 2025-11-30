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
    "layerID": [ 152 ], 
    "makeVisible": false
}
```

> Note: `_value` can be `forwardEnum`, `backwardEnum`, or `targetEnum`. `layerID` is often included by Photoshop but might be optional if selecting purely by relative position.

## Select by Name (Hypothetical)

*If referencing a specific layer by name:*

```json
{
    "_obj": "select",
    "_target": [
        {
            "_ref": "layer",
            "_name": "Background"
        }
    ]
}
```

## Parameters

- `makeVisible`: Boolean, whether to toggle visibility upon selection.
- `_target`: Specifies which layer to select.

