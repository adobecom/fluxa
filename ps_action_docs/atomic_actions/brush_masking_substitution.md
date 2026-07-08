# Brush / Manual Masking Substitution

**When the tutorial says: "select the brush, paint on the mask to hide/reveal…"**

The Photoshop API **cannot do freehand brush strokes**. If you create a mask and then "select the
brush tool," no painting happens — so a `hideAll` mask leaves the layer fully hidden and a
`revealAll` mask does nothing. Either way the effect fails to render. Substitute the brush's
*intent* with the deterministic actions below.

## Substitution Table

| Tutorial says… | Do this instead | Why |
|----------------|-----------------|-----|
| "Paint black to hide the dark background of the overlay so it blends into the portrait" | Set the overlay layer's **blend mode to `screen` or `lighten`** (see `layer_management/set_layer_properties.md`) | Screen/Lighten automatically drop dark pixels — this IS the double-exposure blend, no brushing needed |
| "Reveal only the subject / erase the overlay around the model" | `autoCutout` → **`revealSelection`** mask on the layer (see `layer_management/create_mask.md`) | Clips the layer to the subject silhouette automatically |
| "Softly fade / lower the effect in an area" | Reduce layer **opacity** (`layer_management/set_opacity.md`) + keep the blend mode | Approximates a soft brush without strokes |
| "Brush to blend two exposures together" | **Blend mode** (`screen`/`lighten`) + reduced **opacity** | Deterministic, valid, renders every time |

## ❌ Do NOT emit these

```json
{ "_obj": "select", "_target": [ { "_ref": "paintbrushTool" } ] }   // no-op without strokes
```
```json
{ "_obj": "make", "at": {"_enum":"channel","_ref":"channel","_value":"mask"},
  "new": {"_class":"channel"},
  "using": {"_enum":"userMaskEnabled","_value":"hideAll"} }          // hides the whole layer forever
```

## ✅ Do this — Double-Exposure blend (fully automatable)

```json
[
    { "_obj": "placeEvent", "null": { "_kind": "local", "_path": "ACTION_JSON_OPTIONS_ADDITIONAL_IMAGES_0" },
      "freeTransformCenterState": { "_enum": "quadCenterState", "_value": "QCSAverage" } },

    { "_obj": "set", "_target": [ { "_enum": "ordinal", "_ref": "layer", "_value": "targetEnum" } ],
      "to": { "_obj": "layer", "mode": { "_enum": "blendMode", "_value": "screen" } } },

    { "_obj": "set", "_target": [ { "_enum": "ordinal", "_ref": "layer", "_value": "targetEnum" } ],
      "to": { "_obj": "layer", "opacity": { "_unit": "percentUnit", "_value": 70.0 } } }
]
```

## Rule of Thumb

**Every layer you create must stay visible and contribute to the result.** Achieve blending with
*blend modes*, *opacity*, and *selection-based (`revealSelection`) masks* — never with a bare
`hideAll`/`revealAll` mask that depends on painting. If a step is purely manual brushwork with no
such equivalent, **skip it** rather than hide the layer.
