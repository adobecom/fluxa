# ActionJSON Documentation Guidelines

This document outlines standards for creating and maintaining Photoshop ActionJSON documentation to ensure the AI agent generates accurate and working action sequences.

## Core Principles

### 1. Show the Most Common Use Case First

The **primary JSON example** in each documentation file should represent the **most common real-world use case**, not the simplest or default option.

**Bad Example:**
```markdown
## JSON Structure
{
    "using": { "_value": "revealAll" }  // Default but rarely useful alone
}
```

**Good Example:**
```markdown
## JSON Structure (Common Use Case)
{
    "using": { "_value": "revealSelection" }  // Most common: mask from selection
}
```

### 2. Include Workflow Context

Each action should explain **when and why** to use it, not just **how**.

**Bad:**
```markdown
Creates a layer mask on the currently selected layer.
```

**Good:**
```markdown
Creates a layer mask on the currently selected layer.

**Common Workflow:** After using `autoCutout` (Select Subject), use this action with 
`"revealSelection"` to convert the selection into a mask that isolates the subject.
```

### 3. Document Related Actions

List actions that commonly precede or follow this action.

```markdown
## Related Actions (Typical Sequence)
1. **Before:** `autoCutout` (Select Subject) - Creates selection
2. **This Action:** `make` (Create Mask) - Converts selection to mask
3. **After:** `set` (Deselect) - Clears the marching ants selection
```

### 4. Provide Complete Working Examples

Include end-to-end examples for common workflows, not just isolated actions.

```markdown
## Complete Workflow: Subject Isolation

### Step 1: Select Subject
{
    "_obj": "autoCutout",
    "sampleAllLayers": false
}

### Step 2: Create Mask from Selection
{
    "_obj": "make",
    "at": { "_enum": "channel", "_ref": "channel", "_value": "mask" },
    "new": { "_class": "channel" },
    "using": { "_enum": "userMaskEnabled", "_value": "revealSelection" }
}

### Step 3: Clear Selection (Deselect)
{
    "_obj": "set",
    "_target": [{ "_ref": "channel", "_property": "selection" }],
    "to": { "_enum": "ordinal", "_value": "none" }
}
```

### 5. Highlight Critical Parameters

Use callouts or warnings for parameters that significantly change behavior.

```markdown
## Parameters

- `using._value`: **CRITICAL - Choose based on workflow:**
    - `"revealSelection"` ⭐ **USE THIS** after Select Subject/Color Range
    - `"revealAll"`: White mask (use for manual painting)
    - `"hideAll"`: Black mask (use for manual reveal)
```

### 6. Include "Don't Forget" Sections

List commonly forgotten follow-up actions.

```markdown
## Don't Forget

After creating a mask from selection, you typically need to:
1. **Deselect** - Clear the selection to remove marching ants
2. **Rename layer** - For clarity in complex compositions
```

## Documentation File Structure

Each `.md` file should follow this structure:

```markdown
# Action Name

**Action:** `actionName`
**Target:** What it operates on
**Menu Location:** Photoshop menu path

Brief description of what this action does.

## Common Workflow

Explain the typical use case and what actions come before/after.

## JSON Structure (Primary Use Case)

Show the most common real-world example first.

## Alternative Variations

Show other valid configurations with explanations of when to use them.

## Parameters

Document all parameters with:
- Type and valid values
- When to use each value
- Default behavior

## Related Actions

List actions commonly used before/after this one.

## Complete Example

Show a full working sequence if applicable.

## Notes

Edge cases, warnings, and tips.
```

## Parameter Value Guidelines

### Selection-to-Mask Workflow
When documenting mask creation after a selection:
- Primary example: `"revealSelection"`
- Explain that `"revealAll"` ignores the selection

### Layer Targeting
- Use `"targetEnum"` for "currently selected layer"
- Use `"_name"` when referencing layers by name
- Use `"_index"` only when position is known

### Ordinal Values for Layer Order
- `"front"` = top of stack
- `"back"` = bottom of stack (above background)
- `"next"` = one position up
- `"previous"` = one position down
