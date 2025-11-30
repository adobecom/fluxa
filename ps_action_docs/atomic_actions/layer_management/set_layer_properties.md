# Set Layer Properties

**Action:** `set`
**Target:** `layer`

Sets properties of the active layer, such as Blend Mode or Name.

## Set Blend Mode

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
        "mode": {
            "_enum": "blendMode",
            "_value": "screen"
        }
    }
}
```

## Rename Layer

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
        "name": "New Name"
    }
}
```

## Parameters

- `to`: (Object) Properties to set.
    - `mode`: Blend mode enum (e.g., `screen`, `normal`, `multiply`).
    - `name`: New name string.

