# Smart Filters (filterFX)

**Action:** `set` with `filterFX` target  
**Target:** Smart Object layer  
**Menu Location:** Filter menu when Smart Object is selected

Smart Filters (filterFX) are non-destructive filters that can be applied to Smart Objects (Smart Layers). Unlike regular filters that permanently alter pixel data, Smart Filters can be edited, reordered, or removed at any time.

## Apply Gaussian Blur as Smart Filter

Applies a Gaussian Blur filter as a Smart Filter to a Smart Object.

```json
[
    {
        "_obj": "set",
        "_target": [
            {
                "_index": 1,
                "_ref": "filterFX"
            },
            {
                "_enum": "ordinal",
                "_ref": "layer",
                "_value": "targetEnum"
            }
        ],
        "filterFX": {
            "_obj": "filterFX",
            "filter": {
                "_obj": "gaussianBlur",
                "radius": {
                    "_unit": "pixelsUnit",
                    "_value": 5
                }
            },
            "enabled": true,
            "name": "Gaussian Blur"
        }
    }
]
```

## Apply Unsharp Mask as Smart Filter

Applies an Unsharp Mask filter as a Smart Filter with specific parameters.

```json
[
    {
        "_obj": "set",
        "_target": [
            {
                "_index": 1,
                "_ref": "filterFX"
            },
            {
                "_enum": "ordinal",
                "_ref": "layer",
                "_value": "targetEnum"
            }
        ],
        "filterFX": {
            "_obj": "filterFX",
            "filter": {
                "_obj": "unsharpMask",
                "amount": {
                    "_unit": "percentUnit",
                    "_value": 150
                },
                "radius": {
                    "_unit": "pixelsUnit",
                    "_value": 1.5
                },
                "threshold": 0
            },
            "enabled": true,
            "name": "Unsharp Mask"
        }
    }
]
```

## Apply Multiple Smart Filters

Applies multiple filters as a stack of Smart Filters.

```json
[
    {
        "_obj": "set",
        "_target": [
            {
                "_index": 1,
                "_ref": "filterFX"
            },
            {
                "_enum": "ordinal",
                "_ref": "layer",
                "_value": "targetEnum"
            }
        ],
        "filterFX": {
            "_obj": "filterFX",
            "filter": {
                "_obj": "gaussianBlur",
                "radius": {
                    "_unit": "pixelsUnit",
                    "_value": 2
                }
            },
            "enabled": true,
            "name": "Blur"
        }
    },
    {
        "_obj": "set",
        "_target": [
            {
                "_index": 2,
                "_ref": "filterFX"
            },
            {
                "_enum": "ordinal",
                "_ref": "layer",
                "_value": "targetEnum"
            }
        ],
        "filterFX": {
            "_obj": "filterFX",
            "filter": {
                "_obj": "levels",
                "presetKind": {
                    "_enum": "presetKindType",
                    "_value": "presetKindDefault"
                },
                "autoNeutralize": false
            },
            "enabled": true,
            "name": "Levels"
        }
    }
]
```

## Enable/Disable Smart Filter

Toggles the visibility of a Smart Filter.

```json
[
    {
        "_obj": "set",
        "_target": [
            {
                "_index": 1,
                "_ref": "filterFX"
            },
            {
                "_enum": "ordinal",
                "_ref": "layer",
                "_value": "targetEnum"
            }
        ],
        "filterFX": {
            "_obj": "filterFX",
            "enabled": false
        }
    }
]
```

## Delete Smart Filter

Removes a Smart Filter from the layer.

```json
[
    {
        "_obj": "delete",
        "_target": [
            {
                "_index": 1,
                "_ref": "filterFX"
            },
            {
                "_enum": "ordinal",
                "_ref": "layer",
                "_value": "targetEnum"
            }
        ]
    }
]
```

## Parameters

### FilterFX Object Structure

-   `_obj`: `"filterFX"` - Indicates this is a Smart Filter
-   `filter`: Object - The actual filter parameters (varies by filter type)
-   `enabled`: Boolean - Whether the filter is active (`true`) or disabled (`false`)
-   `name`: String (optional) - Custom name for the filter
-   `blendOptions`: Object (optional) - Blending options for the filter
    -   `mode`: Object - Blend mode
        -   `_enum`: `"blendMode"`
        -   `_value`: String (e.g., `"normal"`, `"multiply"`)
    -   `opacity`: Object - Opacity percentage
        -   `_unit`: `"percentUnit"`
        -   `_value`: Number (0-100)

### Target Structure

-   `_target`: Array containing two references
    -   First element: Filter index reference
        -   `_index`: Integer - Filter position in stack (1-based)
        -   `_ref`: `"filterFX"`
    -   Second element: Layer reference
        -   `_enum`: `"ordinal"`
        -   `_ref`: `"layer"`
        -   `_value`: `"targetEnum"` (currently selected layer)

## Common Filter Types

### Gaussian Blur
```json
{
    "_obj": "gaussianBlur",
    "radius": {
        "_unit": "pixelsUnit",
        "_value": 5
    }
}
```

### Unsharp Mask
```json
{
    "_obj": "unsharpMask",
    "amount": {
        "_unit": "percentUnit",
        "_value": 150
    },
    "radius": {
        "_unit": "pixelsUnit",
        "_value": 1.5
    },
    "threshold": 0
}
```

### Levels
```json
{
    "_obj": "levels",
    "presetKind": {
        "_enum": "presetKindType",
        "_value": "presetKindDefault"
    },
    "autoNeutralize": false
}
```

### Hue/Saturation
```json
{
    "_obj": "hueSaturation",
    "colorize": false,
    "master": {
        "hue": 0,
        "saturation": 0,
        "lightness": 0
    }
}
```

### Curves
```json
{
    "_obj": "curves",
    "presetKind": {
        "_enum": "presetKindType",
        "_value": "presetKindDefault"
    },
    "adjustment": [
        {
            "horizontal": 0,
            "vertical": 0
        },
        {
            "horizontal": 255,
            "vertical": 255
        }
    ]
}
```

## Notes

- **Smart Objects Required**: Smart Filters can only be applied to Smart Object layers (Smart Layers). Regular pixel layers must first be converted to Smart Objects.
- **Non-destructive**: Smart Filters can be edited, reordered, enabled/disabled, or deleted without affecting the original image data.
- **Filter Stack**: Multiple Smart Filters can be stacked on a single Smart Object, processed from bottom to top.
- **Index-based**: Filter indices are 1-based (first filter is index 1, second is index 2, etc.).
- **Blend Options**: Each Smart Filter can have its own blend mode and opacity settings.
- **Editability**: Double-clicking a Smart Filter in the Layers panel opens the filter dialog for parameter adjustment.
- **Masking**: Smart Filters respect layer masks and can be masked individually.
- **Performance**: Smart Filters are computed on-demand and cached for performance.
- **Compatibility**: Not all filters support Smart Filter mode - some destructive filters cannot be applied as Smart Filters.
- **Automation**: Smart Filters can be recorded in Actions and replayed consistently.
- **Workflow**: Converting a layer to a Smart Object enables non-destructive filter workflows for complex editing.
- **Memory**: Smart Filters use additional memory as they store both original and filtered versions of the content.

## Converting to Smart Object

Before applying Smart Filters, convert a regular layer to a Smart Object:

```json
[
    {
        "_obj": "newPlacedLayer"
    }
]
```

