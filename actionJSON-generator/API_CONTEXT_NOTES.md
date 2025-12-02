# API Context: Filesystem Operations Handling

## Overview

Fluxa generates Photoshop API JSON actions designed for use in API contexts where documents are already loaded in memory. As a result, filesystem operations are intentionally excluded from generated actions.

## Why This Matters

Traditional Photoshop tutorials often include steps like:
1. "Open image.jpg"
2. Apply emboss filter
3. "Save as output.jpg"

However, in the Photoshop API context:
- Documents are loaded via API calls (not filesystem `open` operations)
- Results are retrieved via API responses (not saved with `save` operations)
- No local filesystem access is available
- File path references don't make sense

## Operations That Are Excluded

### 1. **Open Operations**
```json
{
  "_obj": "open",
  "null": {
    "_kind": "local",
    "_path": "/path/to/image.jpg"
  },
  "template": false
}
```
**Why excluded**: The API caller loads the document before executing actions.

### 2. **Save Operations**
```json
{
  "_obj": "save",
  "as": {"_obj": "JPEG", "quality": 12},
  "in": {
    "_kind": "local",
    "_path": "/path/to/output.jpg"
  }
}
```
**Why excluded**: The API caller retrieves the result after action execution.

### 3. **File Path References**
Any operations that reference local files (displacement maps, patterns, textures, etc.) are also excluded:
```json
{
  "_obj": "someFilter",
  "displacementMap": {
    "_kind": "local",
    "_path": "/path/to/displacement-map.psd"
  }
}
```
**Why excluded**: No filesystem access in API context.

## What IS Generated

Fluxa focuses on generating image manipulation operations that can be executed on an already-loaded document:

✅ **Layer Operations**: make, delete, select, show, hide, move, set  
✅ **Filters**: emboss, blur, sharpen, etc.  
✅ **Color Operations**: fill, reset, exchange  
✅ **Adjustments**: brightness, contrast, hue/saturation  
✅ **Effects**: Various layer effects and styles  

## Example Workflow

### Tutorial Input:
```
1. Open sunflower.jpg
2. Apply emboss filter with amount 200, angle 90, height 5
3. Reduce opacity to 80%
4. Save as embossed-sunflower.jpg
```

### Generated Actions (API Context):
```json
[
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
]
```

**Note**: Steps 1 and 4 (open/save) are omitted.

## API Caller Responsibilities

When using Fluxa-generated actions, the API caller must:

1. **Before execution**:
   - Load the source document into Photoshop via API
   - Ensure the document is in the expected state

2. **During execution**:
   - Execute the generated actions sequentially
   - Handle any errors or exceptions

3. **After execution**:
   - Retrieve the modified document from Photoshop API
   - Save the result if needed (outside of action execution)

## Implementation Details

The exclusion of filesystem operations is enforced at multiple levels:

### 1. System Prompt
The AI is explicitly instructed:
```
**IMPORTANT**: These actions are designed for the Photoshop API context where:
- Documents are loaded via API calls (not filesystem operations)
- Results are retrieved via API (not saved to disk)
- No local filesystem access is available
- Therefore: **NEVER include "open" or "save" operations in your output**
```

### 2. Guidelines
```
3. **CRITICAL - File Operations**: Since these actions run in an API context without filesystem access:
   - **OMIT all "open" operations** - assume the document is already loaded via API
   - **OMIT all "save" operations** - the API caller handles document retrieval
   - **OMIT any operations that reference local file paths**
```

### 3. User Prompt
Each request reinforces:
```
2. **OMIT all "open" and "save" operations** (API context - document is already loaded)
3. **OMIT any file path references** (no filesystem access in API context)
```

### 4. Few-Shot Examples
Training examples demonstrate the correct behavior by showing tutorials with open/save steps being converted to actions that exclude those operations.

## Testing

To verify this behavior:

```bash
cd Fluxa
./venv/bin/python << 'EOF'
from fluxa.prompts.photoshop_actions import get_system_prompt, get_few_shot_examples
import json

# Check system prompt
assert "NEVER include \"open\" or \"save\"" in get_system_prompt()

# Check few-shot examples
examples = get_few_shot_examples()
actions = json.loads(examples[1]["content"])
assert not any(action["_obj"] in ["open", "save"] for action in actions)

print("✓ All checks passed!")
EOF
```

## Benefits

This approach provides:

1. **Clarity**: Generated actions are immediately usable in API contexts
2. **Portability**: No hardcoded file paths to replace
3. **Flexibility**: API caller controls document loading/saving strategy
4. **Simplicity**: Focuses on the core image manipulation steps

## Further Reading

- [README.md](README.md) - Full documentation
- [QUICKSTART.md](QUICKSTART.md) - Getting started guide
- [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) - Project overview
- [src/fluxa/prompts/photoshop_actions.py](src/fluxa/prompts/photoshop_actions.py) - Prompt implementation

---

**Last Updated**: December 2, 2025  
**Version**: 0.1.0

