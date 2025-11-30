# Crop

**Action:** `crop`
**Target:** Document

Crops the image to the current selection.

## JSON Structure

```json
{
    "_obj": "crop",
    "delete": true
}
```

## Parameters

- `delete`: (Boolean) Whether to delete cropped pixels.
- `to`: (Optional) Rectangle coordinates if cropping to specific bounds instead of selection.
    - `top`, `left`, `bottom`, `right` units.

