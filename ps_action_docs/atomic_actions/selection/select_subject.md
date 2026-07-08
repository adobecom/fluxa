# Select Subject

**Action:** `autoCutout`  
**Target:** Active document/layer  
**Menu Location:** Select > Subject

Uses AI-powered neural processing to automatically detect and select the main subject in an image. This feature analyzes the image content and creates a selection around the primary subject, making it useful for quick masking, compositing, and editing workflows.

## Basic Select Subject

Selects the subject using default settings (device processing, current layer only).

```json
{
    "_obj": "autoCutout",
    "sampleAllLayers": false
}
```

## Select Subject with Cloud Processing

Selects the subject using cloud-based processing for potentially better accuracy (requires internet connection).

```json
{
    "_obj": "autoCutout",
    "sampleAllLayers": false,
    "imageProcessingSelectSubjectPrefs": {
        "_enum": "imageProcessingSelectSubjectPrefs",
        "_value": "imageProcessingModeCloud"
    }
}
```

## Select Subject Sampling All Layers

Selects the subject by analyzing all visible layers in the document, not just the active layer.

```json
{
    "_obj": "autoCutout",
    "sampleAllLayers": true,
    "imageProcessingSelectSubjectPrefs": {
        "_enum": "imageProcessingSelectSubjectPrefs",
        "_value": "imageProcessingModeDevice"
    }
}
```

## Example: Select Subject and Apply Effect

Common workflow: select subject, then apply an adjustment layer to the selection.

```json
[
    {
        "_obj": "autoCutout",
        "sampleAllLayers": false
    },
    {
        "_obj": "make",
        "_target": [
            {
                "_ref": "adjustmentLayer"
            }
        ],
        "using": {
            "_obj": "adjustmentLayer",
            "type": {
                "_obj": "blackAndWhite",
                "red": 40,
                "yellow": 60,
                "grain": 40,
                "cyan": 60,
                "blue": 20,
                "magenta": 80,
                "useTint": false,
                "presetKind": {
                    "_enum": "presetKindType",
                    "_value": "presetKindDefault"
                }
            }
        }
    }
]
```

## Parameters

- `sampleAllLayers`: Boolean (optional, default: `false`). When `true`, analyzes all visible layers in the document to determine the subject. When `false`, only analyzes the currently active layer.
- `imageProcessingSelectSubjectPrefs`: Enum object (optional). Specifies the processing method for subject detection.
    - `_enum`: `"imageProcessingSelectSubjectPrefs"`
    - `_value`: One of:
        - `"imageProcessingModeDevice"`: Uses on-device neural processing (default, works offline)
        - `"imageProcessingModeCloud"`: Uses cloud-based processing (requires internet connection, may provide better accuracy)

## Notes

- The action creates a pixel selection around the detected subject. You can then use this selection for masking, applying filters, or other operations.
- If no subject is detected, the action may fail silently or return an error. Always check if a selection was created after running the action.
- Cloud processing requires an internet connection and may take longer but can provide more accurate results for complex images.
- Device processing works offline and is generally faster, but accuracy may vary depending on the image content.
- The selection is created on the active document. Make sure you have a document open before running this action.
- Works best with images containing clear, well-defined subjects (people, animals, objects) against contrasting backgrounds.
- The selection can be refined using Select and Mask or other selection tools after creation.

