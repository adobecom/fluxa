# Solid Color Fill Layer

**Action:** `make`
**Target:** `contentLayer`
**Menu Location:** Layer > New Fill Layer > Solid Color (or the "Solid Color…" option in the Adjustments/Fill layer menu)

Creates a **Solid Color fill layer** — a full-canvas layer filled with a single RGB color. Because it is a fill layer (not a pixel layer), it comes with its own layer mask and can be re-colored non-destructively. Commonly used as a background wash, a color tint, or a base color that other layers clip to.

## JSON Structure

```json
{
    "_obj": "make",
    "_target": [
        {
            "_ref": "contentLayer"
        }
    ],
    "using": {
        "_obj": "contentLayer",
        "type": {
            "_obj": "solidColorLayer",
            "color": {
                "_obj": "RGBColor",
                "red": 82.0,
                "grain": 154.0,
                "blue": 159.0
            }
        }
    }
}
```

## ⚠️ Color Channel Naming (Photoshop quirk)

The RGB color object uses these keys — note that **green is keyed `grain`**, not `green`:

- `red`   → Red   channel (0.0 – 255.0)
- `grain` → **Green** channel (0.0 – 255.0)  ← easy to get wrong
- `blue`  → Blue  channel (0.0 – 255.0)

Values are floats in the `0.0`–`255.0` range.

## Common Workflow: Background Color Behind a Composite

**Typical sequence:** select the background/base layer, add a solid color fill above it as a colored backdrop, then (optionally) move it into position.

```json
[
    {
        "_obj": "select",
        "_target": [
            { "_ref": "layer", "_name": "Background" }
        ]
    },
    {
        "_obj": "make",
        "_target": [ { "_ref": "contentLayer" } ],
        "using": {
            "_obj": "contentLayer",
            "type": {
                "_obj": "solidColorLayer",
                "color": { "_obj": "RGBColor", "red": 20.0, "grain": 30.0, "blue": 60.0 }
            }
        }
    }
]
```

To position the fill layer below the current layer after creating it, follow with a `move`:

```json
{
    "_obj": "move",
    "_target": [ { "_enum": "ordinal", "_ref": "layer", "_value": "targetEnum" } ],
    "to":      { "_enum": "ordinal", "_ref": "layer", "_value": "previous" }
}
```

## Parameters

- `using.type._obj`: `"solidColorLayer"` — identifies this as a Solid Color fill layer.
- `using.type.color`: RGB color object.
    - `_obj`: `"RGBColor"`
    - `red`, `grain` (green), `blue`: floats `0.0`–`255.0`.

## Notes

- The new fill layer is **automatically selected** after creation and is created **above** the currently active layer.
- In tutorials the color is often chosen from the image with the **eyedropper / Color Picker** — that sampling step is interactive and cannot be reproduced in ActionJSON. Supply an explicit RGB value instead (e.g. a color that matches the described mood, or a neutral tone).
- This is a **fill layer**, so it is non-destructive: it can be re-colored, masked, or blended without affecting pixel layers.
- Related fill/content layer types use the same `make → contentLayer → type` structure (e.g. `gradientLayer` for a Gradient fill layer).

## Related Actions

| Sequence | Action | Purpose |
|----------|--------|---------|
| Before | `select` | Target the background/base layer first |
| **This** | `make` (contentLayer / solidColorLayer) | Create the Solid Color fill layer |
| After | `move` | Reorder the fill layer (e.g. send below) |
| After | `set` (blend mode / opacity) | Blend the color into the composite |
