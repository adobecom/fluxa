# Convert to Smart Object

**Action:** `newPlacedLayer`  
**Target:** Selected layer(s)  
**Menu Location:** Layer > Smart Objects > Convert to Smart Object

Converts one or more selected layers into a Smart Object. Smart Objects preserve the original layer data, allowing you to apply non-destructive transformations, filters, and edits. Multiple layers can be converted into a single Smart Object, and the Smart Object can be edited independently.

## Convert Selected Layer to Smart Object

Converts the currently selected layer(s) to a Smart Object.

```json
{
    "_obj": "newPlacedLayer"
}
```

## Convert Specific Layer to Smart Object

Converts a specific layer (by index) to a Smart Object.

```json
{
    "_obj": "newPlacedLayer",
    "_target": [
        {
            "_ref": "layer",
            "_index": 2
        }
    ]
}
```

## Convert Layer by Name to Smart Object

Converts a layer identified by name to a Smart Object.

```json
{
    "_obj": "newPlacedLayer",
    "_target": [
        {
            "_ref": "layer",
            "_name": "My Layer"
        }
    ]
}
```

## Convert Multiple Layers to Single Smart Object

Converts multiple selected layers into a single Smart Object.

```json
{
    "_obj": "newPlacedLayer",
    "_target": [
        {
            "_enum": "ordinal",
            "_ref": "layer",
            "_value": "targetEnum"
        }
    ]
}
```

## Convert Smart Object to Layers

Converts a Smart Object back to regular layers (rasterizes the Smart Object).

```json
{
    "_obj": "placedLayerConvertToLayers",
    "_target": [
        {
            "_enum": "ordinal",
            "_ref": "layer",
            "_value": "targetEnum"
        }
    ]
}
```

## Parameters

### Main Structure

-   `_obj`: `"newPlacedLayer"` - Action type for converting layers to Smart Objects
-   `_target`: Array (optional) - Layer reference(s) to convert. If omitted, uses currently selected layer(s)

### Target Layer Reference (`_target` array, optional)

If provided, specifies which layer(s) to convert:
-   `_enum`: `"ordinal"` with `_value`: `"targetEnum"` - Currently selected layer(s)
-   `_ref`: `"layer"` with `_index`: Integer - Layer by index
-   `_ref`: `"layer"` with `_id`: Integer - Layer by unique ID
-   `_ref`: `"layer"` with `_name`: String - Layer by name

### Convert to Layers (`placedLayerConvertToLayers`)

-   `_obj`: `"placedLayerConvertToLayers"` - Action type for converting Smart Object back to layers
-   `_target`: Array containing a Smart Object layer reference

## Notes

- Smart Objects preserve the original layer data, allowing non-destructive editing.
- Multiple layers can be converted into a single Smart Object - all selected layers will be combined.
- When multiple layers are converted, they are merged into a single Smart Object document.
- Smart Objects can be transformed (scaled, rotated, skewed) without losing quality.
- Filters applied to Smart Objects become "Smart Filters" that can be edited or removed later.
- Smart Objects can be duplicated, and all instances share the same source data (changes to one affect all).
- The Smart Object's contents can be edited by double-clicking the layer thumbnail.
- Converting a Smart Object back to layers (`placedLayerConvertToLayers`) is a destructive operation - it rasterizes the Smart Object.
- Background layers can be converted to Smart Objects (they become regular layers in the process).
- Text layers, shape layers, and adjustment layers can all be converted to Smart Objects.
- Smart Objects maintain their position and appearance after conversion.
- The Smart Object will have the same name as the original layer (or "Smart Object" if multiple layers were converted).

