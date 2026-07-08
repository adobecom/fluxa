# Render Clouds

**Action:** `clouds`
**Target:** Active layer
**Menu Location:** Filter > Render > Clouds

Generates a random cloud/fog pattern on the active layer using the current
**foreground and background colors**. Commonly used (on its own layer, then set to a
blend mode like Screen) to add atmospheric fog, mist, or smoke to a composite.

## ⚠️ This is NOT "Difference Clouds"

- `clouds` → **Filter > Render > Clouds** (replaces layer content with a fresh
  foreground↔background cloud pattern). Use this when the tutorial says "Render Clouds".
- `differenceClouds` → **Filter > Render > Difference Clouds** (blends a cloud pattern
  with existing pixels using Difference mode). Only use this if the tutorial explicitly
  says "Difference Clouds". See `filters/difference_clouds.md`.

## JSON Structure

The Clouds filter takes no parameters — it uses the current foreground/background colors.

```json
{
    "_obj": "clouds"
}
```

## Common Workflow: Atmospheric Fog

Clouds render between the foreground and background colors. For classic black↔white
fog, create a new layer, then render clouds, then blend with Screen:

```json
[
    { "_obj": "make", "_target": [ { "_ref": "layer" } ] },
    { "_obj": "clouds" },
    { "_obj": "set",
      "_target": [ { "_enum": "ordinal", "_ref": "layer", "_value": "targetEnum" } ],
      "to": { "_obj": "layer", "mode": { "_enum": "blendMode", "_value": "screen" } } }
]
```

## Notes

- The pattern is **random** each time — you cannot control the exact shape.
- Output colors are the current **foreground → background** colors. Tutorials usually set
  foreground=black, background=white before rendering; with the API you generally can't
  set the swatch colors, so expect a black↔white cloud pattern by default.
- Put clouds on their **own layer** and use a blend mode (Screen lightens, Multiply
  darkens) so they composite over the image instead of replacing it.

## Related Actions

| Sequence | Action | Purpose |
|----------|--------|---------|
| Before | `make` (new layer) | Give the clouds their own layer |
| **This** | `clouds` | Render the cloud pattern |
| After | `set` (blend mode: screen/multiply) | Composite the fog over the image |
| After | `set` (opacity) | Dial down the intensity |
