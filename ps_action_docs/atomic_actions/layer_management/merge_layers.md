# Merge Layers

**Action:** `mergeLayersNew` or `mergeVisible`
**Target:** None (implicitly targets selected layers)

Merges the currently selected layers (or the active layer/group) into a single layer.

## Merge Selected Layers

Merges the currently selected layers into one.

```json
{
  "_obj": "mergeLayersNew"
}
```

## Merge Visible (Stamp Visible)

Merges all visible layers into a new layer (if `duplicate` is true) or flattens them (if `duplicate` is false/absent). This is often known as "Stamp Visible" (Cmd+Option+Shift+E) when duplicating.

```json
{
    "_obj": "mergeVisible",
    "duplicate": true
}
```

## Parameters

- `duplicate`: (Boolean) If `true`, creates a new merged layer on top of existing layers (non-destructive). If `false` or omitted for `mergeVisible`, it merges visible layers into one (destructive/flatten).
