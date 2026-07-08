# Layer Via Copy (Ctrl+J on a Selection)

**Action:** `copyToLayer`
**Target:** Active layer + active selection
**Menu Location:** Layer > New > Layer Via Copy (shortcut: **Ctrl/Cmd + J**)

Copies the **currently selected pixels** of the active layer into a brand-new layer, positioned directly above the source layer. This is the action Photoshop performs when you press **Ctrl+J with an active selection**.

## ⚠️ CRITICAL: `copyToLayer` vs `duplicate`

These are NOT the same and are a common source of broken effects:

| You want... | Use | Result |
|-------------|-----|--------|
| Copy **only the selected subject/region** to a new layer (Ctrl+J after a selection) | ✅ `copyToLayer` | New layer contains just the selected pixels; the rest is transparent |
| Copy the **entire layer** (Ctrl+J with NO selection) | `duplicate` | New layer is a full copy of the whole layer |

➡️ **When the tutorial says "select the subject, then press Ctrl+J", you MUST use `copyToLayer`, NOT `duplicate`.** Using `duplicate` copies the whole rectangular layer, so any subsequent clipping mask or blend will clip to the full frame instead of the subject silhouette.

## JSON Structure

`copyToLayer` takes no parameters. It acts on the active layer and the active selection.

```json
{
    "_obj": "copyToLayer"
}
```

## Common Workflow: Isolate a Subject onto its Own Layer

**Typical sequence (double exposure, subject isolation, etc.):**
1. `autoCutout` — Select the subject (Select > Subject)
2. `copyToLayer` — Ctrl+J: copy the selected subject to a new layer
3. Continue with compositing (place second image, clipping mask, blend mode, ...)

```json
[
    {
        "_obj": "autoCutout",
        "sampleAllLayers": false
    },
    {
        "_obj": "copyToLayer"
    }
]
```

## Parameters

- None. The action operates implicitly on the active layer and the current selection.

## Notes

- **Requires an active selection** for the "copy just the selection" behaviour. If no selection is active, `copyToLayer` copies the entire layer (equivalent to Ctrl+J with nothing selected).
- The new layer is **automatically selected** after the action — do NOT add a `select` action immediately after.
- The new layer is placed **directly above** the source layer in the stack.
- The original selection is consumed; there is no need to `deselect` afterward (the marching ants are cleared by the copy).

## Related Actions

| Sequence | Action | Purpose |
|----------|--------|---------|
| Before | `autoCutout` | Select Subject (AI selection) |
| Before | `colorRange` | Select by color |
| **This** | `copyToLayer` | Copy selection to a new layer (Ctrl+J) |
| After | `placeEvent` | Place a second image to composite |
| After | `groupEvent` | Create a clipping mask against the copied subject |
