"""
Prompt templates for AI generation of Photoshop API actions
"""

from typing import Dict, Any
import json


SYSTEM_PROMPT = """You are an expert at converting Photoshop tutorial instructions into Photoshop API JSON action format.

**IMPORTANT**: These actions are designed for the Photoshop API context where:
- Documents are loaded via API calls (not filesystem operations)
- Results are retrieved via API (not saved to disk)
- No local filesystem access is available
- Therefore: **NEVER include "open" or "save" operations in your output**

# Photoshop API JSON Format

Each action is a JSON object with the following structure:
- `_obj`: The operation name (e.g., "emboss", "make", "set", etc.)
- Additional properties specific to the operation
- Complex values use objects with type indicators like `_enum`, `_unit`, `_value`, `_kind`, `_path`, `_ref`, etc.

# Multiple Input Images

When a tutorial requires multiple images (e.g., compositing, blending two photos):
1. The FIRST image is automatically loaded as the base/background layer
2. ADDITIONAL images must be explicitly placed using the `placeEvent` action
3. Reference additional images using: `ACTION_JSON_OPTIONS_ADDITIONAL_IMAGES_X` where X is 0-based index

**Example - Placing second image (from additionalImages[0])**:
```json
{
  "_obj": "placeEvent",
  "freeTransformCenterState": {
    "_enum": "quadCenterState",
    "_value": "QCSAverage"
  },
  "null": {
    "_kind": "local",
    "_path": "ACTION_JSON_OPTIONS_ADDITIONAL_IMAGES_0"
  },
  "offset": {
    "_obj": "offset",
    "horizontal": {"_unit": "pixelsUnit", "_value": 0},
    "vertical": {"_unit": "pixelsUnit", "_value": 0}
  }
}
```

**After placing, select layers using ordinal references**:
- `{"_enum": "ordinal", "_ref": "layer", "_value": "targetEnum"}` - current/top layer
- `{"_enum": "ordinal", "_ref": "layer", "_value": "back"}` - background/bottom layer
- `{"_enum": "ordinal", "_ref": "layer", "_index": 1}` - layer by index (0-based from top)

**CRITICAL FOR MULTI-IMAGE TUTORIALS**: 
- Always place additional images FIRST before operating on them
- Use ordinal references instead of layer names when possible
- The placed image becomes the current/target layer

# Well-Supported Operations

## Selection Operations

**Select subject (AI-powered)**:
```json
{"_obj": "autoCutout", "sampleAllLayers": false}
```

**Invert selection**:
```json
{"_obj": "inverse"}
```

**Deselect**:
```json
{
  "_obj": "set",
  "_target": [{"_ref": "channel", "_property": "selection"}],
  "to": {"_enum": "ordinal", "_value": "none"}
}
```

## Filter Operations

**Gaussian blur**:
```json
{
  "_obj": "gaussianBlur",
  "radius": {"_unit": "pixelsUnit", "_value": 10.0}
}
```

**Motion blur**:
```json
{
  "_obj": "motionBlur",
  "angle": {"_unit": "angleUnit", "_value": 0.0},
  "distance": {"_unit": "pixelsUnit", "_value": 20}
}
```

**Add noise**:
```json
{
  "_obj": "addNoise",
  "amount": {"_unit": "percentUnit", "_value": 10.0},
  "distribution": {"_enum": "distribution", "_value": "gaussian"},
  "monochromatic": true
}
```

## Adjustment Operations

**Brightness/Contrast**:
```json
{
  "_obj": "brightnessEvent",
  "brightness": 20,
  "contrast": 15,
  "useLegacy": false
}
```

**Hue/Saturation**:
```json
{
  "_obj": "hueSaturation",
  "colorize": false,
  "hue": {"_unit": "angleUnit", "_value": 0.0},
  "saturation": {"_unit": "percentUnit", "_value": 30.0},
  "lightness": {"_unit": "percentUnit", "_value": 0.0}
}
```

**Vibrance**:
```json
{
  "_obj": "vibrance",
  "vibrance": 25,
  "saturation": 10
}
```

**Desaturate**:
```json
{"_obj": "desaturate"}
```

## Layer Operations

**Set layer opacity**:
```json
{
  "_obj": "set",
  "_target": [{"_enum": "ordinal", "_ref": "layer", "_value": "targetEnum"}],
  "to": {"_obj": "layer", "opacity": {"_unit": "percentUnit", "_value": 75.0}}
}
```

**Set blend mode**:
```json
{
  "_obj": "set",
  "_target": [{"_enum": "ordinal", "_ref": "layer", "_value": "targetEnum"}],
  "to": {"_obj": "layer", "mode": {"_enum": "blendMode", "_value": "screen"}}
}
```

**Create new layer**:
```json
{"_obj": "make", "_target": [{"_ref": "layer"}]}
```

**Fill with color**:
```json
{
  "_obj": "fill",
  "mode": {"_enum": "blendMode", "_value": "normal"},
  "opacity": {"_unit": "percentUnit", "_value": 100.0},
  "using": {"_enum": "fillContents", "_value": "white"}
}
```

**Select layer**:
```json
{"_obj": "select", "_target": [{"_enum": "ordinal", "_ref": "layer", "_value": "back"}]}
```

## Text Operations

**Create text layer** (use "LOREM IPSUM" as default text):
```json
{
  "_obj": "make",
  "_target": [{"_ref": "textLayer"}],
  "using": {
    "_obj": "textLayer",
    "textKey": "LOREM IPSUM",
    "textStyleRange": [{
      "from": 0,
      "to": 11,
      "textStyle": {
        "_obj": "textStyle",
        "size": {"_unit": "pointsUnit", "_value": 72.0},
        "color": {
          "_obj": "RGBColor",
          "red": 255.0,
          "grain": 255.0,
          "blue": 255.0
        }
      }
    }]
  }
}
```

**CRITICAL for text tutorials**:
- Always use "LOREM IPSUM" as the default text content
- The text length must match the "to" value in textStyleRange (from 0 to length)
- Common text: "LOREM IPSUM" = 11 chars (0 to 11)
- For longer text: "LOREM IPSUM DOLOR SIT AMET" = 26 chars (0 to 26)
- Avoid text effects requiring displacement maps or smart objects (not supported in API)

# Important Guidelines

1. Output ONLY a valid JSON array of action objects
2. Each step in the tutorial should map to one or more actions
3. **CRITICAL - File Operations**: Since these actions run in an API context without filesystem access:
   - **OMIT all "open" operations** - assume the document is already loaded via API
   - **OMIT all "save" operations** - the API caller handles document retrieval
   - **OMIT any operations that reference local file paths** (e.g., loading displacement maps, patterns, or textures from disk)
   - Focus only on the image manipulation steps that can be executed on an already-loaded document
4. **KEEP IT SIMPLE**: Use the simplest, most direct operations that work reliably in the API:
   - Prefer basic operations over complex/experimental features
   - **AVOID these operations**: convertToSmartObject, contentAwareFill, tiltBlur, minimum, modifySelection, displace, mergeVisible, duplicate (with layers)
   - **Text effects**: For text tutorials, create simple text layers with "LOREM IPSUM" - avoid displacement maps and smart object effects
   - Stick to well-documented operations: gaussianBlur, autoCutout, inverse, set, make, fill, adjustments, text layers
5. **USE ORDINAL REFERENCES**: When selecting layers, prefer ordinal references:
   - `{"_enum": "ordinal", "_ref": "layer", "_value": "targetEnum"}` - current layer
   - `{"_enum": "ordinal", "_ref": "layer", "_value": "back"}` - background layer
6. Preserve parameter values when specified in the tutorial
7. Use default values for unspecified parameters
8. Maintain the order of operations from the tutorial
9. Skip non-Photoshop steps (like "download the file" or "watch the video")
10. If a tutorial step is unclear or not a standard Photoshop operation, skip it
11. Do not include explanations or comments, only the JSON array

# Common Effect Patterns

## Background Blur Effect

Tutorial steps: "Select subject", "Blur background"
→ Use this simple pattern:

```json
[
  {"_obj": "autoCutout", "sampleAllLayers": false},
  {"_obj": "inverse"},
  {"_obj": "gaussianBlur", "radius": {"_unit": "pixelsUnit", "_value": 15.0}},
  {
    "_obj": "set",
    "_target": [{"_ref": "channel", "_property": "selection"}],
    "to": {"_enum": "ordinal", "_value": "none"}
  }
]
```

## Color Adjustments

Tutorial steps: "Increase saturation", "Brighten image"
→ Simple pattern:

```json
[
  {"_obj": "hueSaturation", "colorize": false, "saturation": {"_unit": "percentUnit", "_value": 30.0}},
  {"_obj": "brightnessEvent", "brightness": 20, "contrast": 0, "useLegacy": false}
]
```

## Text Effect (Simple)

Tutorial steps: "Remove background", "Add text with effect"
→ Simple pattern (skip complex displacement/smart object effects):

```json
[
  {"_obj": "autoCutout", "sampleAllLayers": false},
  {"_obj": "inverse"},
  {"_obj": "fill", "mode": {"_enum": "blendMode", "_value": "normal"}, "opacity": {"_unit": "percentUnit", "_value": 100.0}, "using": {"_enum": "fillContents", "_value": "black"}},
  {"_obj": "set", "_target": [{"_ref": "channel", "_property": "selection"}], "to": {"_enum": "ordinal", "_value": "none"}},
  {
    "_obj": "make",
    "_target": [{"_ref": "textLayer"}],
    "using": {
      "_obj": "textLayer",
      "textKey": "LOREM IPSUM",
      "textStyleRange": [{
        "from": 0,
        "to": 11,
        "textStyle": {
          "_obj": "textStyle",
          "size": {"_unit": "pointsUnit", "_value": 72.0},
          "color": {"_obj": "RGBColor", "red": 255.0, "grain": 255.0, "blue": 255.0}
        }
      }]
    }
  }
]
```

# Output Format

Return a JSON array like this (note: no open/save operations):
```json
[
  {"_obj": "emboss", "amount": 150, "angle": 135, "height": 5},
  {"_obj": "set", "_target": [{"_enum": "ordinal", "_ref": "layer"}], "to": {"_obj": "layer", "opacity": {"_unit": "percentUnit", "_value": 75.0}}},
  {"_obj": "make", "_target": [{"_ref": "layer"}]}
]
```
"""


USER_PROMPT_TEMPLATE = """Convert the following Photoshop tutorial into Photoshop API JSON actions.

Tutorial Source: {source}
Tutorial Type: {source_type}

Tutorial Content:
{content}

Remember to:
1. Extract only Photoshop-specific operations
2. **OMIT all "open" and "save" operations** (API context - document is already loaded)
3. **OMIT any file path references** (no filesystem access in API context)
4. **USE SIMPLE, WELL-SUPPORTED OPERATIONS ONLY**:
   - Use: gaussianBlur, motionBlur, autoCutout, inverse, brightnessEvent, hueSaturation, vibrance, desaturate, make (with textLayer)
   - Avoid: convertToSmartObject, contentAwareFill, tiltBlur, minimum, modifySelection, displace, mergeVisible
   - For background blur: autoCutout → inverse → gaussianBlur → deselect
   - For text: Always use "LOREM IPSUM" as default text, skip displacement maps and smart object effects
5. **FOR MULTIPLE IMAGES**: If tutorial mentions adding/placing/importing/overlaying another image:
   - Use placeEvent with ACTION_JSON_OPTIONS_ADDITIONAL_IMAGES_0 for the second image
   - Use ACTION_JSON_OPTIONS_ADDITIONAL_IMAGES_1 for third image, etc.
   - Then select layers using ordinal references (targetEnum, back, or _index)
6. Maintain the order of steps
7. Use appropriate parameter values
8. Return ONLY the JSON array, no explanations

Output the JSON array now:"""


def get_system_prompt() -> str:
    """Get the system prompt for Photoshop action generation"""
    return SYSTEM_PROMPT


def get_user_prompt(content: str, source: str, source_type: str) -> str:
    """
    Get the user prompt with tutorial content
    
    Args:
        content: Tutorial text content
        source: Source URL
        source_type: Type of source (youtube or web)
        
    Returns:
        Formatted user prompt
    """
    return USER_PROMPT_TEMPLATE.format(
        source=source,
        source_type=source_type,
        content=content
    )


def get_few_shot_examples() -> list:
    """
    Get few-shot examples for better AI understanding
    
    Returns:
        List of example messages
    """
    return [
        {
            "role": "user",
            "content": """Convert the following Photoshop tutorial into Photoshop API JSON actions.

Tutorial Source: example.com/tutorial
Tutorial Type: web

Tutorial Content:
1. Open the sunflower.jpg image
2. Apply an emboss filter with amount 200, angle 90, and height 5
3. Reduce opacity to 80%
4. Save the result as embossed-flower.jpg

Output the JSON array now:"""
        },
        {
            "role": "assistant",
            "content": json.dumps([
                {
                    "_obj": "emboss",
                    "amount": 200,
                    "angle": 90,
                    "height": 5
                },
                {
                    "_obj": "set",
                    "_target": [{"_enum": "ordinal", "_ref": "layer"}],
                    "to": {
                        "_obj": "layer",
                        "opacity": {"_unit": "percentUnit", "_value": 80.0}
                    }
                }
            ], indent=2)
        },
        {
            "role": "user",
            "content": """Convert the following Photoshop tutorial into Photoshop API JSON actions.

Tutorial Source: example.com/blend-tutorial
Tutorial Type: web

Tutorial Content:
1. Open the base landscape image
2. Add a texture overlay image on top
3. Set the overlay blend mode to Screen
4. Reduce overlay opacity to 60%
5. Select the base layer
6. Increase brightness by 20
7. Save the final result

Output the JSON array now:"""
        },
        {
            "role": "assistant",
            "content": json.dumps([
                {
                    "_obj": "placeEvent",
                    "freeTransformCenterState": {
                        "_enum": "quadCenterState",
                        "_value": "QCSAverage"
                    },
                    "null": {
                        "_kind": "local",
                        "_path": "ACTION_JSON_OPTIONS_ADDITIONAL_IMAGES_0"
                    },
                    "offset": {
                        "_obj": "offset",
                        "horizontal": {"_unit": "pixelsUnit", "_value": 0},
                        "vertical": {"_unit": "pixelsUnit", "_value": 0}
                    }
                },
                {
                    "_obj": "set",
                    "_target": [{"_enum": "ordinal", "_ref": "layer", "_value": "targetEnum"}],
                    "to": {
                        "_obj": "layer",
                        "mode": {"_enum": "blendMode", "_value": "screen"}
                    }
                },
                {
                    "_obj": "set",
                    "_target": [{"_enum": "ordinal", "_ref": "layer", "_value": "targetEnum"}],
                    "to": {
                        "_obj": "layer",
                        "opacity": {"_unit": "percentUnit", "_value": 60.0}
                    }
                },
                {
                    "_obj": "select",
                    "_target": [{"_enum": "ordinal", "_ref": "layer", "_value": "back"}],
                    "makeVisible": False
                },
                {
                    "_obj": "brightnessEvent",
                    "brightness": 20,
                    "contrast": 0,
                    "useLegacy": False
                }
            ], indent=2)
        },
        {
            "role": "user",
            "content": """Convert the following Photoshop tutorial into Photoshop API JSON actions.

Tutorial Source: example.com/blur-tutorial
Tutorial Type: web

Tutorial Content:
1. Open your portrait photo
2. Select the subject using AI
3. Invert the selection to get the background
4. Apply a Gaussian blur of 15 pixels to blur the background
5. Create a nice bokeh effect
6. Save the result

Output the JSON array now:"""
        },
        {
            "role": "assistant",
            "content": json.dumps([
                {
                    "_obj": "autoCutout",
                    "sampleAllLayers": False
                },
                {
                    "_obj": "inverse"
                },
                {
                    "_obj": "gaussianBlur",
                    "radius": {
                        "_unit": "pixelsUnit",
                        "_value": 15.0
                    }
                },
                {
                    "_obj": "set",
                    "_target": [
                        {
                            "_ref": "channel",
                            "_property": "selection"
                        }
                    ],
                    "to": {
                        "_enum": "ordinal",
                        "_value": "none"
                    }
                }
            ], indent=2)
        },
        {
            "role": "user",
            "content": """Convert the following Photoshop tutorial into Photoshop API JSON actions.

Tutorial Source: example.com/text-effect
Tutorial Type: web

Tutorial Content:
1. Open your image
2. Select the subject and remove the background  
3. Create a text layer with your desired text
4. Make the text bold and set size to 72pt
5. Apply a displacement map effect to the text
6. Convert to smart object for non-destructive editing
7. Save your work

Output the JSON array now:"""
        },
        {
            "role": "assistant",
            "content": json.dumps([
                {
                    "_obj": "autoCutout",
                    "sampleAllLayers": False
                },
                {
                    "_obj": "inverse"
                },
                {
                    "_obj": "fill",
                    "mode": {
                        "_enum": "blendMode",
                        "_value": "normal"
                    },
                    "opacity": {
                        "_unit": "percentUnit",
                        "_value": 100.0
                    },
                    "using": {
                        "_enum": "fillContents",
                        "_value": "black"
                    }
                },
                {
                    "_obj": "set",
                    "_target": [
                        {
                            "_ref": "channel",
                            "_property": "selection"
                        }
                    ],
                    "to": {
                        "_enum": "ordinal",
                        "_value": "none"
                    }
                },
                {
                    "_obj": "make",
                    "_target": [
                        {
                            "_ref": "textLayer"
                        }
                    ],
                    "using": {
                        "_obj": "textLayer",
                        "textKey": "LOREM IPSUM",
                        "textStyleRange": [
                            {
                                "from": 0,
                                "to": 11,
                                "textStyle": {
                                    "_obj": "textStyle",
                                    "size": {
                                        "_unit": "pointsUnit",
                                        "_value": 72.0
                                    },
                                    "fontPostScriptName": "Arial-BoldMT",
                                    "color": {
                                        "_obj": "RGBColor",
                                        "red": 255.0,
                                        "grain": 255.0,
                                        "blue": 255.0
                                    }
                                }
                            }
                        ]
                    }
                }
            ], indent=2)
        }
    ]


