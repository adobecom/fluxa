# Text Layer

**Action:** `make`  
**Target:** `textLayer`  
**Menu Location:** Layer > New > Type Layer / Text Tool

Creates a new text layer with specified text content, font properties, and styling options. Text layers are vector-based and remain editable, allowing you to modify the text content and formatting at any time.

## Create Basic Text Layer

Creates a simple text layer with default settings.

```json
{
    "_obj": "make",
    "_target": [
        {
            "_ref": "textLayer"
        }
    ],
    "using": {
        "_obj": "textLayer",
        "textKey": "Hello, World!",
        "textStyleRange": [
            {
                "_obj": "textStyleRange",
                "from": 0,
                "to": 14,
                "textStyle": {
                    "_obj": "textStyle",
                    "size": {
                        "_unit": "pixelsUnit",
                        "_value": 24
                    }
                }
            }
        ],
        "paragraphStyleRange": [
            {
                "_obj": "paragraphStyleRange",
                "from": 0,
                "to": 14,
                "paragraphStyle": {
                    "_obj": "paragraphStyle",
                    "align": {
                        "_enum": "alignmentType",
                        "_value": "left"
                    }
                }
            }
        ]
    }
}
```

## Create Text Layer with Custom Font and Color

Creates a text layer with specific font, size, color, and position.

```json
{
    "_obj": "make",
    "_target": [
        {
            "_ref": "textLayer"
        }
    ],
    "using": {
        "_obj": "textLayer",
        "name": "My Text Layer",
        "textKey": "Photoshop",
        "textClickPoint": {
            "_obj": "paint",
            "horizontal": {
                "_unit": "percentUnit",
                "_value": 50.0
            },
            "vertical": {
                "_unit": "percentUnit",
                "_value": 50.0
            }
        },
        "textStyleRange": [
            {
                "_obj": "textStyleRange",
                "from": 0,
                "to": 10,
                "textStyle": {
                    "_obj": "textStyle",
                    "fontPostScriptName": "Arial-BoldMT",
                    "size": {
                        "_unit": "pixelsUnit",
                        "_value": 48
                    },
                    "color": {
                        "_obj": "RGBColor",
                        "red": 255.0,
                        "grain": 0.0,
                        "blue": 0.0
                    }
                }
            }
        ],
        "paragraphStyleRange": [
            {
                "_obj": "paragraphStyleRange",
                "from": 0,
                "to": 10,
                "paragraphStyle": {
                    "_obj": "paragraphStyle",
                    "align": {
                        "_enum": "alignmentType",
                        "_value": "center"
                    }
                }
            }
        ]
    }
}
```

## Create Text Layer with Layer Properties

Creates a text layer with additional layer properties like opacity and blend mode.

```json
{
    "_obj": "make",
    "_target": [
        {
            "_ref": "textLayer"
        }
    ],
    "using": {
        "_obj": "textLayer",
        "name": "Styled Text",
        "opacity": {
            "_unit": "percentUnit",
            "_value": 75
        },
        "mode": {
            "_enum": "blendMode",
            "_value": "multiply"
        },
        "textKey": "Sample Text",
        "textStyleRange": [
            {
                "_obj": "textStyleRange",
                "from": 0,
                "to": 12,
                "textStyle": {
                    "_obj": "textStyle",
                    "size": {
                        "_unit": "pixelsUnit",
                        "_value": 36
                    }
                }
            }
        ],
        "paragraphStyleRange": [
            {
                "_obj": "paragraphStyleRange",
                "from": 0,
                "to": 12,
                "paragraphStyle": {
                    "_obj": "paragraphStyle"
                }
            }
        ]
    }
}
```

## Parameters

### Main Structure

-   `_obj`: `"make"` - Action type for creating a new layer
-   `_target`: Array containing a reference object with `_ref: "textLayer"`
-   `using`: Object containing the text layer properties

### Text Layer Properties (`using` object)

-   `_obj`: `"textLayer"` - Specifies this is a text layer
-   `name`: String (optional) - Name of the text layer
-   `textKey`: String - The actual text content to display
-   `textClickPoint`: Object (optional) - Position where the text is placed
    -   `_obj`: `"paint"`
    -   `horizontal`: Object with `_unit` (e.g., `"percentUnit"` or `"pixelsUnit"`) and `_value` (number)
    -   `vertical`: Object with `_unit` and `_value`
-   `opacity`: Object (optional) - Layer opacity
    -   `_unit`: `"percentUnit"`
    -   `_value`: Number (0-100)
-   `mode`: Object (optional) - Blend mode
    -   `_enum`: `"blendMode"`
    -   `_value`: Blend mode name (e.g., `"normal"`, `"multiply"`, `"screen"`)

### Text Style Range (`textStyleRange` array)

Each element in the array defines styling for a range of characters:

-   `_obj`: `"textStyleRange"`
-   `from`: Integer - Starting character index (0-based)
-   `to`: Integer - Ending character index (exclusive, typically `textKey.length + 1`)
-   `textStyle`: Object containing:
    -   `_obj`: `"textStyle"`
    -   `fontPostScriptName`: String (optional) - PostScript name of the font (e.g., `"Arial-BoldMT"`, `"TimesNewRomanPSMT"`)
    -   `size`: Object (optional) - Font size
        -   `_unit`: `"pixelsUnit"` or `"pointsUnit"`
        -   `_value`: Number
    -   `color`: Object (optional) - Text color
        -   `_obj`: `"RGBColor"`
        -   `red`, `grain` (green), `blue`: Numbers (0-255)

### Paragraph Style Range (`paragraphStyleRange` array)

Each element defines paragraph formatting for a range of characters:

-   `_obj`: `"paragraphStyleRange"`
-   `from`: Integer - Starting character index
-   `to`: Integer - Ending character index
-   `paragraphStyle`: Object containing:
    -   `_obj`: `"paragraphStyle"`
    -   `align`: Object (optional) - Text alignment
        -   `_enum`: `"alignmentType"`
        -   `_value`: `"left"`, `"center"`, `"right"`, or `"justify"`

## Notes

- The `to` value in `textStyleRange` and `paragraphStyleRange` is typically `textKey.length + 1` (the length of the text plus 1).
- Text position (`textClickPoint`) uses percentage units by default, where 50.0 represents the center of the document.
- When using pixel units for position, ensure the values are appropriate for your document dimensions.
- Font PostScript names can be found by inspecting existing text layers or using font enumeration APIs.
- Text layers remain editable - you can modify the text content and formatting after creation.
- Multiple `textStyleRange` entries can be used to apply different styles to different parts of the text.
- The default font if not specified is typically "MyriadPro-Regular" or the system default.
- Text layers support rich formatting including multiple fonts, sizes, and colors within a single layer.

