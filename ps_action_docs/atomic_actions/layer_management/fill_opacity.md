# Fill Opacity

**Action:** `set`  
**Target:** Layer  
**Menu Location:** Layer Properties Panel / Layers Panel

Sets the fill opacity of a layer, which controls the opacity of the layer's content (pixels, shapes, text) without affecting the opacity of layer effects (drop shadows, glows, strokes, etc.). This is useful for creating effects where you want the layer's effects to remain fully visible while reducing the visibility of the layer content itself.

## Set Fill Opacity

Sets the fill opacity of the currently selected layer.

```json
{
    "_obj": "set",
    "_target": [
        {
            "_enum": "ordinal",
            "_ref": "layer",
            "_value": "targetEnum"
        }
    ],
    "to": {
        "_obj": "layer",
        "fillOpacity": {
            "_unit": "percentUnit",
            "_value": 50
        }
    }
}
```

## Set Fill Opacity for Specific Layer

Sets the fill opacity of a layer identified by index.

```json
{
    "_obj": "set",
    "_target": [
        {
            "_ref": "layer",
            "_index": 2
        }
    ],
    "to": {
        "_obj": "layer",
        "fillOpacity": {
            "_unit": "percentUnit",
            "_value": 75
        }
    }
}
```

## Set Fill Opacity for Layer by Name

Sets the fill opacity of a layer identified by name.

```json
{
    "_obj": "set",
    "_target": [
        {
            "_ref": "layer",
            "_name": "My Layer"
        }
    ],
    "to": {
        "_obj": "layer",
        "fillOpacity": {
            "_unit": "percentUnit",
            "_value": 25
        }
    }
}
```

## Set Fill Opacity and Opacity Together

Sets both the regular opacity and fill opacity of a layer simultaneously.

```json
{
    "_obj": "set",
    "_target": [
        {
            "_enum": "ordinal",
            "_ref": "layer",
            "_value": "targetEnum"
        }
    ],
    "to": {
        "_obj": "layer",
        "opacity": {
            "_unit": "percentUnit",
            "_value": 80
        },
        "fillOpacity": {
            "_unit": "percentUnit",
            "_value": 60
        }
    }
}
```

## Parameters

### Main Structure

-   `_obj`: `"set"` - Action type for setting layer properties
-   `_target`: Array containing a layer reference to modify
-   `to`: Object containing the layer properties to set

### Target Layer Reference (`_target` array)

The layer to modify can be specified as:
-   `_enum`: `"ordinal"` with `_value`: `"targetEnum"` - Currently selected layer
-   `_ref`: `"layer"` with `_index`: Integer - Layer by index
-   `_ref`: `"layer"` with `_id`: Integer - Layer by unique ID
-   `_ref`: `"layer"` with `_name`: String - Layer by name

### Layer Properties (`to` object)

-   `_obj`: `"layer"` - Specifies this is a layer property object
-   `fillOpacity`: Object (optional) - Fill opacity value
    -   `_unit`: `"percentUnit"` - Unit type for percentage
    -   `_value`: Number (0-100) - Fill opacity percentage

## Notes

- Fill opacity values range from 0 to 100, where 0 is completely transparent and 100 is fully opaque.
- Fill opacity affects only the layer's content (pixels, shapes, text), not layer effects like drop shadows, glows, strokes, or bevels.
- Regular `opacity` affects both the layer content and its effects together.
- The combination of `opacity` and `fillOpacity` allows for fine-grained control: `opacity` controls overall visibility, while `fillOpacity` controls content visibility independently of effects.
- Fill opacity is particularly useful for text layers with effects - you can reduce the text visibility while keeping effects fully visible.
- Background layers cannot have their fill opacity changed directly (they must be converted to regular layers first).
- When setting fill opacity, the value is stored internally as 0-255, but the action JSON uses 0-100 percentage values.
- Fill opacity can be set independently of regular opacity, allowing for creative effects where effects remain visible while content fades.

