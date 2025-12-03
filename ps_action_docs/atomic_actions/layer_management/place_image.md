# Place Image (Import Additional Image)

**Action:** `placeEvent`  
**Target:** Document  
**Menu Location:** File > Place Embedded / File > Place Linked

Places (imports) an additional image into the current document as a new layer. This is essential for compositing workflows where you need to combine multiple images.

## Common Workflow

**Most common use case:** Import a second image into a document for compositing, blending, or masking effects. The placed image becomes a new layer that can be transformed, masked, and blended with other layers.

**Important:** The Photoshop API provides multiple images through:
- First image → Automatically loaded as the base document
- Additional images → Must be explicitly placed using `placeEvent`

## ⚠️ CRITICAL: Layer Selection After placeEvent

**After `placeEvent`, the placed layer is AUTOMATICALLY SELECTED.**

❌ **DO NOT** add a `select` action after `placeEvent` - it is unnecessary and will likely select the WRONG layer.

✅ **Correct pattern:**
```json
{ "_obj": "placeEvent", ... },
{ "_obj": "removeBackground" }  // Operates on the placed layer (already selected)
```

❌ **WRONG pattern:**
```json
{ "_obj": "placeEvent", ... },
{ "_obj": "select", "_target": [{ "_value": "forwardEnum" }] },  // WRONG! Will select wrong layer
{ "_obj": "removeBackground" }  // Now operates on wrong layer!
```

**Proceed directly to your next operation after `placeEvent`.**

## JSON Structure (Primary Use Case - Place Second Image)

⭐ **Use this to import the second image** - uses the API placeholder for additional images.

```json
{
    "_obj": "placeEvent",
    "null": {
        "_kind": "local",
        "_path": "ACTION_JSON_OPTIONS_ADDITIONAL_IMAGES_0"
    },
    "freeTransformCenterState": {
        "_enum": "quadCenterState",
        "_value": "QCSAverage"
    },
    "offset": {
        "_obj": "offset",
        "horizontal": {
            "_unit": "pixelsUnit",
            "_value": 0
        },
        "vertical": {
            "_unit": "pixelsUnit",
            "_value": 0
        }
    }
}
```

## Place Third Image

For a third image, use index 1:

```json
{
    "_obj": "placeEvent",
    "null": {
        "_kind": "local",
        "_path": "ACTION_JSON_OPTIONS_ADDITIONAL_IMAGES_1"
    },
    "freeTransformCenterState": {
        "_enum": "quadCenterState",
        "_value": "QCSAverage"
    },
    "offset": {
        "_obj": "offset",
        "horizontal": {
            "_unit": "pixelsUnit",
            "_value": 0
        },
        "vertical": {
            "_unit": "pixelsUnit",
            "_value": 0
        }
    }
}
```

## Parameters

### Main Structure

-   `_obj`: `"placeEvent"` - Action type for placing/importing an image
-   `null`: Object containing the file path reference
    -   `_kind`: `"local"` - Indicates a local file path
    -   `_path`: String - **Use these placeholders:**
        -   `"ACTION_JSON_OPTIONS_ADDITIONAL_IMAGES_0"` - Second image (first additional)
        -   `"ACTION_JSON_OPTIONS_ADDITIONAL_IMAGES_1"` - Third image (second additional)
        -   `"ACTION_JSON_OPTIONS_ADDITIONAL_IMAGES_2"` - Fourth image, etc.
-   `freeTransformCenterState`: Object - Transform center point
    -   `_enum`: `"quadCenterState"`
    -   `_value`: `"QCSAverage"` - Center of the placed image
-   `offset`: Object (optional) - Position offset from center
    -   `horizontal`: Horizontal offset in pixels
    -   `vertical`: Vertical offset in pixels

## Related Actions

| Sequence | Action | Purpose |
|----------|--------|---------|
| **This** | `placeEvent` | Import additional image as new layer |
| After | `transform` | Resize/position the placed image |
| After | `make` (mask) | Create mask for blending |
| After | Select gradient tool | Prepare for gradient mask |
| After | `syntheticGenHarmonize` | Harmonize colors with background |

## Complete Example: Two-Image Gradient Blend

### Step 1: Place Second Image
```json
{
    "_obj": "placeEvent",
    "null": {
        "_kind": "local",
        "_path": "ACTION_JSON_OPTIONS_ADDITIONAL_IMAGES_0"
    },
    "freeTransformCenterState": {
        "_enum": "quadCenterState",
        "_value": "QCSAverage"
    },
    "offset": {
        "_obj": "offset",
        "horizontal": {
            "_unit": "pixelsUnit",
            "_value": 0
        },
        "vertical": {
            "_unit": "pixelsUnit",
            "_value": 0
        }
    }
}
```

### Step 2: Create Mask on Placed Layer
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

### Step 3: Select Gradient Tool
```json
{
    "_obj": "select",
    "_target": [
        {
            "_ref": "gradientTool"
        }
    ]
}
```

## Notes

- The placed image becomes a new layer on top of the layer stack
- **Always use the placeholder** `ACTION_JSON_OPTIONS_ADDITIONAL_IMAGES_X` - the Photoshop API replaces this with the actual image path at runtime
- The index is 0-based: 0 = second image, 1 = third image, etc.
- **⚠️ The placed layer is AUTOMATICALLY SELECTED after placement - DO NOT add a `select` action after `placeEvent`**
- For multi-image compositing workflows (blending, gradient masks, etc.), this action is **required** to import additional images
- The first/primary image is automatically loaded as the base document - you don't need `placeEvent` for it

