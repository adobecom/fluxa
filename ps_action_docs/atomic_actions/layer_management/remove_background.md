# Remove Background

**Action:** `removeBackground`  
**Target:** Currently selected layer  
**Menu Location:** Quick Actions panel, Layer Properties panel, or Context bar

Automatically removes the background from the selected layer using AI-powered subject detection. The feature creates a layer mask that hides the background while preserving the foreground subject. This is useful for isolating objects, people, or subjects from their backgrounds.

## Basic Remove Background

Removes the background from the currently selected layer.

```json
{
    "_obj": "removeBackground"
}
```

## Remove Background with Layer Rename

Removes the background and renames the layer to "Foreground".

```json
[
    {
        "_obj": "removeBackground"
    },
    {
        "_obj": "set",
        "_target": [
            {
                "_enum": "ordinal",
                "_ref": "layer",
                "_value": "targetEnum"
            }
        ],
        "to": {
            "_obj": "layer",
            "name": "Foreground"
        }
    }
]
```

## Remove Background Workflow Example

A complete workflow that duplicates the layer, rasterizes it, removes the background, and hides the original layer.

```json
[
    {
        "_obj": "duplicate",
        "_target": [
            {
                "_enum": "ordinal",
                "_ref": "layer",
                "_value": "targetEnum"
            }
        ],
        "version": 5
    },
    {
        "_obj": "rasterizeLayer",
        "_target": [
            {
                "_enum": "ordinal",
                "_ref": "layer",
                "_value": "targetEnum"
            }
        ]
    },
    {
        "_obj": "removeBackground"
    },
    {
        "_obj": "hide",
        "null": [
            {
                "_ref": "layer",
                "_id": 123
            }
        ]
    }
]
```

## Parameters

### Main Structure

-   `_obj`: `"removeBackground"` - Action type for removing background
-   No additional parameters are required - the action operates on the currently selected layer

## Notes

- Remove Background uses AI-powered subject detection to automatically identify and mask the background.
- The feature creates a layer mask that hides the background pixels while preserving the foreground subject.
- The action operates on the currently selected layer - ensure the correct layer is selected before executing.
- If the layer already has a layer mask, it will be replaced with the new background removal mask (you may be prompted to confirm).
- The feature works best on layers with clear subjects and distinct backgrounds.
- Remove Background may use cloud-based processing for better accuracy, which requires an internet connection.
- The action is non-destructive - the original pixels remain, but are hidden by the mask.
- You can refine the mask manually after removal using brush tools or selection tools.
- The feature may take a few seconds to process, especially for high-resolution images.
- Remove Background works on pixel layers - text layers, shape layers, or Smart Objects may need to be rasterized first.
- The action can be combined with other actions in a batchPlay array for complex workflows.
- After removing the background, the layer name is often changed to "Foreground" to indicate the background has been removed.
- The mask created by Remove Background can be edited, inverted, or deleted like any other layer mask.
- For best results, use images with good contrast between subject and background.
- The feature may not work perfectly on complex backgrounds or subjects with fine details like hair or fur - manual refinement may be needed.

