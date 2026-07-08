# Stroke Layer Style

**Action:** `set`  
**Target:** Layer (via `layerEffects` property)  
**Menu Location:** Layer > Layer Style > Stroke

Applies a stroke (outline) effect to a layer. The stroke can be applied as a solid color, gradient, or pattern, and can be positioned outside, inside, or centered on the layer's edge.

## Common Workflow

**Most common use case:** Add a white outline stroke to text layers for visibility and contrast against backgrounds. This is especially useful for text overlay effects where the text needs to stand out.

## JSON Structure (Primary Use Case - White Stroke)

⭐ **Use this format for text outline effects** - creates a visible white stroke.

```json
{
    "_obj": "set",
    "_target": [
        {
            "_property": "layerEffects",
            "_ref": "property"
        },
        {
            "_enum": "ordinal",
            "_ref": "layer",
            "_value": "targetEnum"
        }
    ],
    "to": {
        "_obj": "layerEffects",
        "frameFX": {
            "_obj": "frameFX",
            "enabled": true,
            "present": true,
            "showInDialog": true,
            "style": {
                "_enum": "frameStyle",
                "_value": "outsetFrame"
            },
            "size": {
                "_unit": "pixelsUnit",
                "_value": 6
            },
            "mode": {
                "_enum": "blendMode",
                "_value": "normal"
            },
            "opacity": {
                "_unit": "percentUnit",
                "_value": 100
            },
            "paintType": {
                "_enum": "frameFill",
                "_value": "solidColor"
            },
            "color": {
                "_obj": "RGBColor",
                "red": 255.0,
                "grain": 255.0,
                "blue": 255.0
            },
            "overprint": false
        },
        "scale": {
            "_unit": "percentUnit",
            "_value": 100
        }
    }
}
```

## Stroke with Gradient Fill

Applies a stroke with a gradient fill.

```json
{
    "_obj": "set",
    "_target": [
        {
            "_property": "layerEffects",
            "_ref": "property"
        },
        {
            "_enum": "ordinal",
            "_ref": "layer",
            "_value": "targetEnum"
        }
    ],
    "to": {
        "_obj": "layerEffects",
        "frameFX": {
            "_obj": "frameFX",
            "enabled": true,
            "present": true,
            "showInDialog": true,
            "style": {
                "_enum": "frameStyle",
                "_value": "centeredFrame"
            },
            "size": {
                "_unit": "pixelsUnit",
                "_value": 5
            },
            "mode": {
                "_enum": "blendMode",
                "_value": "normal"
            },
            "opacity": {
                "_unit": "percentUnit",
                "_value": 100
            },
            "paintType": {
                "_enum": "frameFill",
                "_value": "gradientFill"
            },
            "gradient": {
                "_obj": "gradientClassEvent",
                "name": "Foreground to Background"
            },
            "type": {
                "_enum": "gradientType",
                "_value": "linear"
            },
            "reverse": false,
            "dither": false,
            "scale": {
                "_unit": "percentUnit",
                "_value": 100
            },
            "align": true,
            "linked": true,
            "offset": {
                "_obj": "paint",
                "horizontal": {
                    "_unit": "percentUnit",
                    "_value": 0
                },
                "vertical": {
                    "_unit": "percentUnit",
                    "_value": 0
                }
            },
            "overprint": false
        },
        "scale": {
            "_unit": "percentUnit",
            "_value": 100
        }
    }
}
```

## Stroke with Pattern Fill

Applies a stroke with a pattern fill.

```json
{
    "_obj": "set",
    "_target": [
        {
            "_property": "layerEffects",
            "_ref": "property"
        },
        {
            "_ref": "layer",
            "_index": 1
        }
    ],
    "to": {
        "_obj": "layerEffects",
        "frameFX": {
            "_obj": "frameFX",
            "enabled": true,
            "present": true,
            "showInDialog": true,
            "style": {
                "_enum": "frameStyle",
                "_value": "insetFrame"
            },
            "size": {
                "_unit": "pixelsUnit",
                "_value": 8
            },
            "mode": {
                "_enum": "blendMode",
                "_value": "multiply"
            },
            "opacity": {
                "_unit": "percentUnit",
                "_value": 75
            },
            "paintType": {
                "_enum": "frameFill",
                "_value": "patternFill"
            },
            "pattern": {
                "_obj": "pattern",
                "name": "Pattern Name"
            },
            "scale": {
                "_unit": "percentUnit",
                "_value": 50
            },
            "linked": true,
            "align": true,
            "phase": {
                "_obj": "paint",
                "horizontal": {
                    "_unit": "percentUnit",
                    "_value": 0
                },
                "vertical": {
                    "_unit": "percentUnit",
                    "_value": 0
                }
            },
            "overprint": false
        },
        "scale": {
            "_unit": "percentUnit",
            "_value": 100
        }
    }
}
```

## Parameters

### Main Structure

-   `_obj`: `"set"` - Action type for setting layer properties
-   `_target`: Array containing property reference and layer reference
    -   First element: `{ "_property": "layerEffects", "_ref": "property" }` - Specifies we're setting layer effects
    -   Second element: Layer reference (ordinal, index, id, or name)
-   `to`: Object containing the layer effects configuration

### Layer Effects Object (`to` object)

-   `_obj`: `"layerEffects"` - Specifies this is a layer effects object
-   `scale`: Object - Overall scale for all effects
    -   `_unit`: `"percentUnit"`
    -   `_value`: Number (typically 100)
-   `frameFX`: Object - Stroke effect configuration

### Stroke Effect (`frameFX` object)

-   `_obj`: `"frameFX"` - Specifies this is a stroke effect
-   `enabled`: Boolean - Whether the effect is enabled
-   `present`: Boolean - Whether the effect is present/active
-   `showInDialog`: Boolean - Whether to show in layer style dialog
-   `style`: Object - Stroke position
    -   `_enum`: `"frameStyle"`
    -   `_value`: One of:
        -   `"outsetFrame"` - Stroke appears outside the layer edge
        -   `"insetFrame"` - Stroke appears inside the layer edge
        -   `"centeredFrame"` - Stroke is centered on the layer edge
-   `size`: Object - Stroke width/thickness
    -   `_unit`: `"pixelsUnit"`
    -   `_value`: Number (stroke width in pixels)
-   `mode`: Object - Blend mode for the stroke
    -   `_enum`: `"blendMode"`
    -   `_value`: Blend mode name (e.g., `"normal"`, `"multiply"`, `"screen"`)
-   `opacity`: Object - Stroke opacity
    -   `_unit`: `"percentUnit"`
    -   `_value`: Number (0-100)
-   `paintType`: Object - Fill type for the stroke
    -   `_enum`: `"frameFill"`
    -   `_value`: One of:
        -   `"solidColor"` - Solid color fill
        -   `"gradientFill"` - Gradient fill
        -   `"patternFill"` - Pattern fill
-   `overprint`: Boolean - Whether to use overprint (knockout if false)

### Solid Color Fill (when `paintType` is `"solidColor"`)

-   `color`: Object - Stroke color
    -   `_obj`: `"RGBColor"`
    -   `red`, `grain` (green), `blue`: Numbers (0-255)

### Gradient Fill (when `paintType` is `"gradientFill"`)

-   `gradient`: Object - Gradient definition
    -   `_obj`: `"gradientClassEvent"`
    -   `name`: String - Name of the gradient preset
-   `type`: Object (optional) - Gradient type
    -   `_enum`: `"gradientType"`
    -   `_value`: `"linear"`, `"radial"`, `"angle"`, `"reflected"`, `"diamond"`, or `"shapeBurst"`
-   `reverse`: Boolean (optional) - Reverse the gradient direction
-   `dither`: Boolean (optional) - Apply dithering
-   `scale`: Object - Gradient scale
    -   `_unit`: `"percentUnit"`
    -   `_value`: Number (typically 100)
-   `align`: Boolean - Align gradient with layer
-   `linked`: Boolean - Link gradient with layer
-   `offset`: Object - Gradient offset
    -   `_obj`: `"paint"`
    -   `horizontal`, `vertical`: Objects with `_unit` (`"percentUnit"`) and `_value` (number)

### Pattern Fill (when `paintType` is `"patternFill"`)

-   `pattern`: Object - Pattern definition
    -   `_obj`: `"pattern"`
    -   `name`: String - Name of the pattern preset
-   `scale`: Object - Pattern scale
    -   `_unit`: `"percentUnit"`
    -   `_value`: Number (typically 100)
-   `linked`: Boolean - Link pattern with layer
-   `align`: Boolean - Align pattern with layer
-   `phase`: Object - Pattern phase offset
    -   `_obj`: `"paint"`
    -   `horizontal`, `vertical`: Objects with `_unit` (`"percentUnit"`) and `_value` (number)

## Notes

- Stroke is a layer effect, so it must be set via the `layerEffects` property, not directly on the layer.
- The `scale` property at the `layerEffects` level affects all effects on the layer, while `scale` within `frameFX` affects only the stroke effect.
- Stroke styles:
    -   `outsetFrame`: Stroke extends outward from the layer edge (most common)
    -   `insetFrame`: Stroke extends inward from the layer edge
    -   `centeredFrame`: Stroke is centered on the layer edge (half inside, half outside)
- The stroke effect works on any layer type including text layers, shape layers, and pixel layers.
- Multiple stroke effects can be applied using `frameFXMulti` array instead of `frameFX`.
- When using gradient or pattern fills, ensure the gradient/pattern name matches an existing preset in Photoshop.
- The `overprint` property controls whether the stroke uses knockout (false) or overprint (true) behavior.
- Stroke effects are non-destructive and can be modified or removed at any time.
- The stroke size is specified in pixels and is affected by the document resolution.

