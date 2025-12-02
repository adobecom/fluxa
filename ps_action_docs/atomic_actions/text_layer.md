# Text Layer

**Action:** `make`  
**Target:** `textLayer`  
**Menu Location:** Layer > New > Type Layer / Text Tool

Creates a new text layer with specified text content, font properties, and styling options. Text layers are vector-based and remain editable, allowing you to modify the text content and formatting at any time.

## Common Workflow

**Most common use case:** Create a centered text layer for titles, watermarks, or overlay effects.

**Important:** Always include `textClickPoint` to position the text. Without it, text appears at the default position (usually top-left), which is rarely what you want.

## JSON Structure (Primary Use Case - Centered Text)

⭐ **Use this format for most text effects** - creates centered, impactful text.

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
        "textKey": "TITLE",
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
                "to": 5,
                "textStyle": {
                    "_obj": "textStyle",
                    "fontPostScriptName": "Impact",
                    "size": {
                        "_unit": "pixelsUnit",
                        "_value": 100
                    },
                    "color": {
                        "_obj": "RGBColor",
                        "red": 255.0,
                        "grain": 255.0,
                        "blue": 255.0
                    }
                }
            }
        ],
        "paragraphStyleRange": [
            {
                "_obj": "paragraphStyleRange",
                "from": 0,
                "to": 5,
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

**Default text:** Use `"HELLO WORLD"` if no specific text is mentioned in the transcript.

**Recommended Fonts for Impact:**
- `"Impact"` - Bold, condensed, highly visible (best for titles)
- `"Arial-BoldMT"` - Clean, widely available
- `"Helvetica-Bold"` - Professional, modern
- `"BebasNeue-Regular"` - Popular for posters (if installed)

## Alternative: Basic Text Layer (No Position)

⚠️ **Warning:** Without `textClickPoint`, text appears at the default position (top-left). Only use this if you plan to manually position the text afterward.

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
                "to": 13,
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
                "to": 13,
                "paragraphStyle": {
                    "_obj": "paragraphStyle"
                }
            }
        ]
    }
}
```

## Alternative: Text with Layer Properties

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
                "to": 11,
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
                "to": 11,
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

## Parameters

### Main Structure

-   `_obj`: `"make"` - Action type for creating a new layer
-   `_target`: Array containing a reference object with `_ref: "textLayer"`
-   `using`: Object containing the text layer properties

### Text Layer Properties (`using` object)

-   `_obj`: `"textLayer"` - Specifies this is a text layer
-   `name`: String (optional) - Name of the text layer
-   `textKey`: String - The actual text content to display
-   `textClickPoint`: Object - **CRITICAL for positioning** - Where the text is placed
    -   `_obj`: `"paint"`
    -   `horizontal`: Object with `_unit` (`"percentUnit"` recommended) and `_value` (50.0 = center)
    -   `vertical`: Object with `_unit` and `_value` (50.0 = center)
-   `opacity`: Object (optional) - Layer opacity
    -   `_unit`: `"percentUnit"`
    -   `_value`: Number (0-100)
-   `mode`: Object (optional) - Blend mode
    -   `_enum`: `"blendMode"`
    -   `_value`: Blend mode name (e.g., `"normal"`, `"multiply"`, `"screen"`)

### Text Click Point (`textClickPoint` object)

**Always include this for predictable text positioning!**

-   `_obj`: `"paint"`
-   `horizontal`: Position from left edge
    -   `_unit`: `"percentUnit"` (recommended) or `"pixelsUnit"`
    -   `_value`: 50.0 = center, 0 = left edge, 100 = right edge
-   `vertical`: Position from top edge
    -   `_unit`: `"percentUnit"` (recommended) or `"pixelsUnit"`
    -   `_value`: 50.0 = center, 0 = top edge, 100 = bottom edge

### Text Style Range (`textStyleRange` array)

Each element in the array defines styling for a range of characters:

-   `_obj`: `"textStyleRange"`
-   `from`: Integer - Starting character index (0-based)
-   `to`: Integer - Ending character index (should equal text length)
-   `textStyle`: Object containing:
    -   `_obj`: `"textStyle"`
    -   `fontPostScriptName`: String - **Font choice matters!** Recommended fonts:
        -   `"Impact"` ⭐ **Best for titles** - Bold, condensed, high visibility
        -   `"Arial-BoldMT"` - Clean, universally available
        -   `"Helvetica-Bold"` - Professional, modern look
        -   `"BebasNeue-Regular"` - Trendy poster font (if available)
    -   `size`: Object - Font size
        -   `_unit`: `"pixelsUnit"` or `"pointsUnit"`
        -   `_value`: Number - **Use 100px** as default for balanced visibility
    -   `color`: Object - Text color (white recommended for overlays)
        -   `_obj`: `"RGBColor"`
        -   `red`, `grain` (green), `blue`: Numbers (0-255)
        -   **White: 255, 255, 255** (most versatile for overlays)

### Paragraph Style Range (`paragraphStyleRange` array)

Each element defines paragraph formatting for a range of characters:

-   `_obj`: `"paragraphStyleRange"`
-   `from`: Integer - Starting character index
-   `to`: Integer - Ending character index
-   `paragraphStyle`: Object containing:
    -   `_obj`: `"paragraphStyle"`
    -   `align`: Object - Text alignment
        -   `_enum`: `"alignmentType"`
        -   `_value`: `"left"`, `"center"` (recommended for titles), `"right"`, or `"justify"`

## Don't Forget

When creating text for overlay effects:
1. **Always include `textClickPoint`** with 50.0/50.0 for centered text
2. **Use center alignment** in `paragraphStyle` for titles
3. **Use large font sizes** (150-300px) for title effects
4. **Set `to` value** equal to the length of your text

## Notes

- The `to` value in `textStyleRange` and `paragraphStyleRange` should equal the length of `textKey`
- Text position (`textClickPoint`) uses percentage units by default, where 50.0 represents the center of the document
- Font PostScript names can be found by inspecting existing text layers or using font enumeration APIs
- Text layers remain editable - you can modify the text content and formatting after creation
- Multiple `textStyleRange` entries can be used to apply different styles to different parts of the text
- The default font if not specified is typically "MyriadPro-Regular" or the system default
- **White text (255, 255, 255)** is commonly used for overlay effects
