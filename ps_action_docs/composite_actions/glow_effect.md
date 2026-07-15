# Glow Effect (make an object glow / light effect)

**When the tutorial says:** "make it glow", "glow effect", "add light/glow to the
[object]", "light source", "glowing [peanut/orb/neon/etc.]".

Render-tested against the `actionJSON` endpoint. The glow is built **deterministically
in code** (`fluxa/effects/glow.py`) once the object to glow is isolated — the pipeline
segments the user-chosen object (SAM/Florence) or falls back to `autoCutout`. The agent's
job is only to **detect** that this is a glow tutorial and identify the object.

## ⚠️ Isolation is mandatory
Linear Dodge is **additive**. Applying the glow to the whole frame blows it out to white.
The glow must come from an **isolated object** on its own layer. Never glow the flat
background.

## The recipe (isolate → duplicate → Linear Dodge → stacked Gaussian Blur)

```json
[
  { "_obj": "autoCutout", "sampleAllLayers": false },
  { "_obj": "copyToLayer" },

  { "_obj": "duplicate", "_target": [ { "_enum": "ordinal", "_ref": "layer", "_value": "targetEnum" } ] },
  { "_obj": "set", "_target": [ { "_enum": "ordinal", "_ref": "layer", "_value": "targetEnum" } ],
    "to": { "_obj": "layer", "mode": { "_enum": "blendMode", "_value": "linearDodge" } } },
  { "_obj": "gaussianBlur", "radius": { "_unit": "pixelsUnit", "_value": 20.0 } },
  { "_obj": "set", "_target": [ { "_enum": "ordinal", "_ref": "layer", "_value": "targetEnum" } ],
    "to": { "_obj": "layer", "opacity": { "_unit": "percentUnit", "_value": 70.0 } } },

  { "_obj": "duplicate", "_target": [ { "_enum": "ordinal", "_ref": "layer", "_value": "targetEnum" } ] },
  { "_obj": "gaussianBlur", "radius": { "_unit": "pixelsUnit", "_value": 90.0 } },

  { "_obj": "duplicate", "_target": [ { "_enum": "ordinal", "_ref": "layer", "_value": "targetEnum" } ] },
  { "_obj": "gaussianBlur", "radius": { "_unit": "pixelsUnit", "_value": 250.0 } }
]
```

- **`linearDodge`** = Linear Dodge (Add) — verified against the Photoshop source
  (`enumPsLinearDodge`). It brightens where the glow layers overlap.
- Increasing blur radii (20 → 90 → 250) create tight-to-wide soft falloff. Scale the
  radii with image resolution; "stronger/bigger glow" → larger radii and/or more layers.
- Darken the background first (Curves/Brightness) if the tutorial does — but **never**
  with a Color Lookup / 3D-LUT preset (the API ignores those).

## Do NOT
- ❌ Do not `mergeVisible` / flatten (keeps the glow editable; avoids the flat-color bug).
- ❌ Do not glow without isolating first.
- ❌ Do not use Color Lookup to darken — use Curves/Brightness.
<!-- doc -->
