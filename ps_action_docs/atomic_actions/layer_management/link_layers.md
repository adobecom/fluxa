# Link Layers

**Action:** `linkSelectedLayers`, `unlinkSelectedLayers`, `link`, or `unlink`  
**Target:** Selected layer(s) or specific layer(s)  
**Menu Location:** Layer > Link Layers / Unlink Layers

Links layers together so they move, transform, and align together. Linked layers maintain their relationship until explicitly unlinked. This is useful for keeping related layers synchronized during transformations.

## Link Selected Layers

Links all currently selected layers together.

```json
{
    "_obj": "linkSelectedLayers",
    "_target": [
        {
            "_enum": "ordinal",
            "_ref": "layer",
            "_value": "targetEnum"
        }
    ]
}
```

## Unlink Selected Layers

Unlinks all currently selected layers from their link chains.

```json
{
    "_obj": "unlinkSelectedLayers",
    "_target": [
        {
            "_enum": "ordinal",
            "_ref": "layer",
            "_value": "targetEnum"
        }
    ]
}
```

## Link Specific Layers

Links a specific layer to one or more other layers.

```json
{
    "_obj": "link",
    "_target": [
        {
            "_ref": "layer",
            "_index": 1
        }
    ],
    "to": [
        {
            "_ref": "layer",
            "_index": 2
        },
        {
            "_ref": "layer",
            "_index": 3
        }
    ]
}
```

## Link Layers by ID

Links layers using their unique IDs.

```json
{
    "_obj": "link",
    "_target": [
        {
            "_ref": "layer",
            "_id": 123
        }
    ],
    "to": [
        {
            "_ref": "layer",
            "_id": 456
        }
    ]
}
```

## Unlink Specific Layer

Unlinks a specific layer from its link chain.

```json
{
    "_obj": "unlink",
    "_target": [
        {
            "_ref": "layer",
            "_index": 2
        }
    ]
}
```

## Unlink Layer from Specific Layers

Unlinks a layer from specific other layers in its link chain.

```json
{
    "_obj": "unlink",
    "_target": [
        {
            "_ref": "layer",
            "_index": 1
        }
    ],
    "to": [
        {
            "_ref": "layer",
            "_index": 2
        }
    ]
}
```

## Parameters

### Link Selected Layers / Unlink Selected Layers

-   `_obj`: Action type
    -   `"linkSelectedLayers"` - Links all currently selected layers
    -   `"unlinkSelectedLayers"` - Unlinks all currently selected layers
-   `_target`: Array containing a layer reference (typically the selected layer)
    -   `_enum`: `"ordinal"`
    -   `_ref`: `"layer"`
    -   `_value`: `"targetEnum"` (currently selected layer)

### Link Specific Layers (`link` action)

-   `_obj`: `"link"` - Action type for linking specific layers
-   `_target`: Array containing the target layer reference (the layer to link to)
-   `to`: Array containing one or more layer references to link to the target layer
    -   Each element is a layer reference (can use `_index`, `_id`, `_name`, etc.)

### Unlink Specific Layer (`unlink` action)

-   `_obj`: `"unlink"` - Action type for unlinking layers
-   `_target`: Array containing the layer reference to unlink
-   `to`: Array (optional) - If provided, unlinks the target layer from these specific layers. If omitted, unlinks the target layer from all layers in its link chain.

### Layer Reference Options

Layers can be referenced using:
-   `_enum`: `"ordinal"` with `_value`: `"targetEnum"` - Currently selected layer
-   `_ref`: `"layer"` with `_index`: Integer - Layer by index
-   `_ref`: `"layer"` with `_id`: Integer - Layer by unique ID
-   `_ref`: `"layer"` with `_name`: String - Layer by name

## Notes

- Linked layers move, transform, and align together as a group.
- A layer can only be part of one link chain at a time.
- Linking layers creates a bidirectional relationship - all layers in a chain are linked to each other.
- If you try to link layers that are already linked (to different chains), they will be unlinked from their previous chains first.
- The `linkSelectedLayers` action is a toggle - if all selected layers are already linked, it will unlink them instead.
- Unlinking a layer removes it from its link chain but doesn't affect other layers in that chain.
- Layers must be in the same document to be linked together.
- Background layers can be linked, but they behave slightly differently than regular layers.
- Link relationships are preserved when layers are moved, duplicated, or copied.
- Linked layers are indicated in the Layers panel with a link icon.
- The link/unlink actions are non-destructive and can be undone.

