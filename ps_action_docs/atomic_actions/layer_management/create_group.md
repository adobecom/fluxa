# Create Layer Group

**Action:** `make`  
**Target:** `layerSection`

Creates a new layer group (folder) in the layer stack.

## JSON Structure

```json
{
    "_obj": "make",
    "_target": [
        {
            "_ref": "layerSection"
        }
    ],
    "layerSectionEnd": 46,
    "layerSectionStart": 45,
    "name": "Group 1"
}
```

## Parameters

- `name`: The name of the new group.
- `layerSectionStart` / `layerSectionEnd`: Internal indices for the group range (optional/generated).

