# Create Layer Group

**Action:** `make`  
**Target:** `layerSection`

Creates a new layer group (folder) in the layer stack.

## Create Empty Group

Creates a new empty group.

```json
{
    "_obj": "make",
    "_target": [
        {
            "_ref": "layerSection"
        }
    ],
    "name": "Group 1"
}
```

## Group Selected Layers

Creates a new group containing the currently selected layers.

```json
{
    "_obj": "make",
    "_target": [
        {
            "_ref": "layerSection"
        }
    ],
    "from": {
        "_enum": "ordinal",
        "_ref": "layer",
        "_value": "targetEnum"
    },
    "name": "Group from Selection"
}
```

## Parameters

- `name`: The name of the new group.
- `from`: (Optional) If present, specifies that the new group should contain the referenced layers (usually `targetEnum` for currently selected layers).
- `layerSectionStart` / `layerSectionEnd`: (Optional) Internal indices for the group range.
