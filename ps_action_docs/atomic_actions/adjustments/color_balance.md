# Color Balance Adjustment Layer

**Action:** `make` (create) + `set` (configure)
**Target:** `adjustmentLayer`
**Menu Location:** Layer > New Adjustment Layer > Color Balance

Creates a **Color Balance** adjustment layer, which shifts colors independently in
the shadows, midtones, and highlights. Commonly used for color grading and giving a
composite a consistent mood (e.g. cool shadows, warm highlights).

## JSON Structure (Create + Configure)

Create the adjustment layer, then `set` the levels. Each level is a 3-value array
`[Cyan↔Red, Magenta↔Green, Yellow↔Blue]`, each from **-100 to 100**.

```json
[
    {
        "_obj": "make",
        "_target": [ { "_ref": "adjustmentLayer" } ],
        "using": {
            "_obj": "adjustmentLayer",
            "type": {
                "_obj": "colorBalance",
                "shadowLevels": [0, 0, 0],
                "midtoneLevels": [0, 0, 0],
                "highlightLevels": [0, 0, 0],
                "preserveLuminosity": true
            }
        }
    },
    {
        "_obj": "set",
        "_target": [ { "_enum": "ordinal", "_ref": "adjustmentLayer", "_value": "targetEnum" } ],
        "to": {
            "_obj": "colorBalance",
            "shadowLevels": [-7, 30, -10],
            "midtoneLevels": [0, 0, 0],
            "highlightLevels": [-7, -9, 0]
        }
    }
]
```

You can also set the levels directly in the `make` step (skip the separate `set`)
by putting the non-zero arrays into `using.type`.

## Parameters

- `shadowLevels` / `midtoneLevels` / `highlightLevels`: 3-int arrays, each -100..100.
    - index 0: **Cyan (−) ↔ Red (+)**
    - index 1: **Magenta (−) ↔ Green (+)**
    - index 2: **Yellow (−) ↔ Blue (+)**
- `preserveLuminosity`: Boolean — keep overall brightness while shifting color (usually `true`).

## Notes

- As an adjustment layer this is **non-destructive** and affects all layers below it
  unless clipped. To limit it to the layer directly below, follow with a clipping mask
  (`groupEvent`).
- Typical grade: warm the highlights (positive red/yellow → negative blue) and cool the
  shadows (negative red, positive blue) for a cinematic look.

## Related Actions

| Sequence | Action | Purpose |
|----------|--------|---------|
| **This** | `make` (adjustmentLayer / colorBalance) | Create the grade layer |
| After | `set` (colorBalance) | Dial in shadow/midtone/highlight shifts |
| After (optional) | `groupEvent` | Clip the grade to the layer below |
