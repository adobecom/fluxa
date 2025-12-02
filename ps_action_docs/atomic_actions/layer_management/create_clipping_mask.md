# Clipping Mask

**Action:** `groupEvent` (create) or `ungroup` (release)  
**Target:** Active layer  
**Menu Location:** Layer > Create Clipping Mask / Layer > Release Clipping Mask

A clipping mask uses the content of one layer to mask (clip) the layers above it. The bottom layer of a clipping mask acts as the mask, and only the areas within its opaque pixels are visible in the clipped layers above.

## Create Clipping Mask

Creates a clipping mask by clipping the currently selected layer to the layer directly below it.

```json
{
    "_obj": "groupEvent",
    "_target": [
        {
            "_enum": "ordinal",
            "_ref": "layer",
            "_value": "targetEnum"
        }
    ]
}
```

## Release Clipping Mask

Releases the clipping mask relationship, making the layer independent again.

```json
{
    "_obj": "ungroup",
    "_target": [
        {
            "_enum": "ordinal",
            "_ref": "layer",
            "_value": "targetEnum"
        }
    ]
}
```

## Example: Create Clipping Mask with Specific Layer

To clip a specific layer by index or name, you can target it explicitly:

```json
{
    "_obj": "groupEvent",
    "_target": [
        {
            "_ref": "layer",
            "_index": 2
        }
    ]
}
```

Or by layer name:

```json
{
    "_obj": "groupEvent",
    "_target": [
        {
            "_ref": "layer",
            "_name": "Layer 1"
        }
    ]
}
```

## Parameters

-   `_obj`: The action object type.
    -   `"groupEvent"`: Creates a clipping mask (clips the selected layer to the layer below)
    -   `"ungroup"`: Releases the clipping mask relationship
-   `_target`: Array containing the layer reference to operate on.
    -   `_ref`: `"layer"` - Specifies that the target is a layer
    -   `_enum`: `"ordinal"` - Indicates an ordinal reference type
    -   `_value`: `"targetEnum"` - Refers to the currently selected/target layer
    -   Alternative targeting options:
        -   `_index`: Integer - Target layer by its index in the layer stack
        -   `_name`: String - Target layer by its name
        -   `_id`: Integer - Target layer by its unique ID

## Use Case: Text Portrait Effect

In the Text Portrait effect, clipping masks make the photograph visible only inside text letters:

**Layer Stack:**
```
[Curves Adjustment]    ← Clipped to text
[B&W Adjustment]       ← Clipped to text
[Photo Layer]          ← Clipped to text
[Text Layer]           ← Base layer (defines visible area)
[Black Background]
```

To achieve this, select each layer above the text and apply `groupEvent` to clip it.

## Related Actions

- `select` layer - Select the layer to clip before applying
- `make` adjustmentLayer - Adjustment layers are often clipped to base layers
- `set` layer properties - Clipped layers can still have blend modes and opacity

## Notes

- The layer that will be clipped must be selected before creating the clipping mask.
- The clipping mask uses the opaque pixels of the layer directly below the selected layer as the mask.
- Multiple layers can be clipped to the same base layer by selecting them and creating a clipping mask.
- Clipping masks are non-destructive - you can release them at any time without losing the layer content.
- The clipped layer's visibility is constrained to the shape of the layer below it.
- Blend modes and opacity of clipped layers still apply within the clipped area.

