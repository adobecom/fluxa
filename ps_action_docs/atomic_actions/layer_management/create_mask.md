# Create Layer Mask

**Action:** `make`  
**Target:** `channel` (relative to layer)  
**Menu Location:** Layer > Layer Mask > Reveal Selection / Reveal All / Hide All

Creates a layer mask on the currently selected layer. Layer masks control which parts of a layer are visible (white = visible, black = hidden).

## Common Workflow

**Most common use case:** After selecting a subject with `autoCutout` (Select > Subject), create a mask to isolate the subject from the background.

**Typical sequence:**
1. `autoCutout` - Select the subject
2. `make` (this action) with `"revealSelection"` - Convert selection to mask
3. `set` (deselect) - Clear the marching ants

## JSON Structure (Primary Use Case - Mask from Selection)

⭐ **Use this when you have an active selection** (e.g., after Select Subject, Color Range, etc.)

```json
{
    "_obj": "make",
    "at": {
        "_enum": "channel",
        "_ref": "channel",
        "_value": "mask"
    },
    "new": {
        "_class": "channel"
    },
    "using": {
        "_enum": "userMaskEnabled",
        "_value": "revealSelection"
    }
}
```

## Alternative: Reveal All (White Mask)

Use when you want to manually paint the mask later. Creates a white mask that shows everything.

```json
{
    "_obj": "make",
    "at": {
        "_enum": "channel",
        "_ref": "channel",
        "_value": "mask"
    },
    "new": {
        "_class": "channel"
    },
    "using": {
        "_enum": "userMaskEnabled",
        "_value": "revealAll"
    }
}
```

## Alternative: Hide All (Black Mask)

Use when you want to manually reveal parts of the layer. Creates a black mask that hides everything.

```json
{
    "_obj": "make",
    "at": {
        "_enum": "channel",
        "_ref": "channel",
        "_value": "mask"
    },
    "new": {
        "_class": "channel"
    },
    "using": {
        "_enum": "userMaskEnabled",
        "_value": "hideAll"
    }
}
```

## Parameters

- `at`: Specifies where to create the new object.
    - `_enum`: `"channel"`
    - `_ref`: `"channel"`
    - `_value`: `"mask"` - Indicates this is a layer mask
- `new`: The type of object being created.
    - `_class`: `"channel"`
- `using`: **CRITICAL - The initial state of the mask:**
    - `_enum`: `"userMaskEnabled"`
    - `_value`: One of:
        - ⭐ `"revealSelection"` - **USE THIS after Select Subject/Color Range** - White where selected, black elsewhere
        - `"revealAll"` - White mask (shows everything, ignores any selection)
        - `"hideAll"` - Black mask (hides everything)

## Related Actions

| Sequence | Action | Purpose |
|----------|--------|---------|
| Before | `autoCutout` | Select Subject (AI selection) |
| Before | `colorRange` | Select by color |
| **This** | `make` (mask) | Convert selection to mask |
| After | `set` (deselect) | Clear selection (remove marching ants) |

## Complete Example: Subject Isolation Workflow

### Step 1: Select Subject
```json
{
    "_obj": "autoCutout",
    "sampleAllLayers": false
}
```

### Step 2: Create Mask from Selection
```json
{
    "_obj": "make",
    "at": {
        "_enum": "channel",
        "_ref": "channel",
        "_value": "mask"
    },
    "new": {
        "_class": "channel"
    },
    "using": {
        "_enum": "userMaskEnabled",
        "_value": "revealSelection"
    }
}
```

### Step 3: Clear Selection (Deselect)
```json
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
```

## Don't Forget

After creating a mask from a selection:
1. **Deselect** - Always clear the selection to remove marching ants
2. **Rename layer** - Consider renaming for clarity (e.g., "Isolated Subject")

## Notes

- `"revealSelection"` is the most commonly needed option when working with selections
- If you use `"revealAll"` or `"hideAll"` after making a selection, the selection will be IGNORED
- The mask is non-destructive - the original pixels are preserved
- You can edit the mask later by painting with black (hide) or white (reveal)
