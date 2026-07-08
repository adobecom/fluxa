# Fill Layer

**Action:** `fill`
**Target:** None (implicitly targets active layer/selection)

Fills the active layer or selection with a color, pattern, or content-aware fill.

## JSON Structure

```json
{
    "_obj": "fill",
    "mode": {
        "_enum": "blendMode",
        "_value": "normal"
    },
    "opacity": {
        "_unit": "percentUnit",
        "_value": 100.0
    },
    "using": {
        "_enum": "fillContents",
        "_value": "gray"
    }
}
```

## Parameters

- `mode`: (Enum) Blending mode for the fill.
    - `_value`: `normal`, `multiply`, `screen`, etc.
- `opacity`: (Unit) Opacity of the fill (percent).
- `using`: (Enum/Object) What to fill with.
    - `_enum`: `fillContents`
    - `_value`: `gray`, `white`, `black`, `foregroundColor`, `backgroundColor`.

