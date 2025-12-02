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

# Common Operations

1. **Apply emboss filter**:
```json
{"_obj": "emboss", "amount": 100, "angle": 135, "height": 3}
```

2. **Set layer opacity**:
```json
{
  "_obj": "set",
  "_target": [{"_enum": "ordinal", "_ref": "layer"}],
  "to": {"_obj": "layer", "opacity": {"_unit": "percentUnit", "_value": 75.0}}
}
```

3. **Show/Hide layer**:
```json
{"_obj": "show", "null": [{"_enum": "ordinal", "_ref": "layer"}]}
{"_obj": "hide", "null": [{"_enum": "ordinal", "_ref": "layer"}]}
```

4. **Create new layer**:
```json
{"_obj": "make", "_target": [{"_ref": "layer"}]}
```

5. **Delete layer**:
```json
{"_obj": "delete", "_target": [{"_enum": "ordinal", "_ref": "layer"}]}
```

6. **Select layer**:
```json
{"_obj": "select", "_target": [{"_ref": "layer", "_name": "Background"}]}
```

7. **Fill with color**:
```json
{
  "_obj": "fill",
  "mode": {"_enum": "blendMode", "_value": "normal"},
  "opacity": {"_unit": "percentUnit", "_value": 100.0},
  "using": {"_enum": "fillContents", "_value": "foregroundColor"}
}
```

# Important Guidelines

1. Output ONLY a valid JSON array of action objects
2. Each step in the tutorial should map to one or more actions
3. **CRITICAL - File Operations**: Since these actions run in an API context without filesystem access:
   - **OMIT all "open" operations** - assume the document is already loaded via API
   - **OMIT all "save" operations** - the API caller handles document retrieval
   - **OMIT any operations that reference local file paths** (e.g., loading displacement maps, patterns, or textures from disk)
   - Focus only on the image manipulation steps that can be executed on an already-loaded document
4. Preserve parameter values when specified in the tutorial
5. Use default values for unspecified parameters
6. Maintain the order of operations from the tutorial
7. Skip non-Photoshop steps (like "download the file" or "watch the video")
8. If a tutorial step is unclear or not a standard Photoshop operation, skip it
9. Do not include explanations or comments, only the JSON array

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
4. Maintain the order of steps
5. Use appropriate parameter values
6. Return ONLY the JSON array, no explanations

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
        }
    ]


