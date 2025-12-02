# Subject Mask

**Action:** Composite (multiple actions)  
**Target:** Active document  
**Menu Location:** Select > Subject, then Edit > Fill

Creates a black and white mask layer from the detected subject in an image. Useful for compositing, creating silhouettes, or generating displacement maps.

## Subject Mask (White Subject, Black Background)

Creates a mask where the subject is white and the background is black.

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
                "_ref": "layer"
            }
        ]
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
            "_value": "white"
        }
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
    }
]
```

## Inverse Subject Mask (Black Subject, White Background)

Creates a mask where the subject is black and the background is white.

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
                "_ref": "layer"
            }
        ]
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
            "_value": "white"
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
]
```

## Workflow Steps

### 1. Select Subject
- **Action:** `autoCutout`
- **Details:** Uses AI to detect and select the main subject in the image.
- **Reference:** [Select Subject](./select_subject.md)

### 2. Create New Layer
- **Action:** `make` with `layer` target
- **Details:** Creates a new empty layer above the current layer. The selection remains active.
- **Reference:** [Create New Layer](../layer_management/create_new_layer.md)

### 3. Fill Selection
- **Action:** `fill`
- **Details:** Fills the selected area (subject) with white or black depending on the mask type.
- **Reference:** [Fill](../layer_management/fill.md)

### 4. Invert Selection
- **Action:** `inverse`
- **Details:** Inverts the selection so the background is now selected instead of the subject.

### 5. Fill Inverted Selection
- **Action:** `fill`
- **Details:** Fills the inverted selection (background) with the opposite color.
- **Reference:** [Fill](../layer_management/fill.md)

### 6. Deselect
- **Action:** `set` with `selection` property set to `none`
- **Details:** Removes the marching ants selection.

## Parameters

### autoCutout
- `sampleAllLayers`: Boolean. When `false`, only analyzes the active layer. When `true`, analyzes all visible layers.

### fill
- `mode._value`: Blend mode for the fill (`normal`, `multiply`, etc.)
- `opacity._value`: Fill opacity (0-100)
- `using._value`: Fill content (`white`, `black`, `gray`, `foregroundColor`, `backgroundColor`)

### inverse
- No parameters required. Inverts the current selection.

## Use Cases

1. **Displacement Maps:** Use the mask as a displacement map for text or texture effects.
2. **Compositing:** Extract subjects for placement on different backgrounds.
3. **Silhouettes:** Create artistic silhouette effects.
4. **Channel Operations:** Use as an alpha channel for advanced masking.
5. **Print/Cut Files:** Generate high-contrast masks for vinyl cutting or screen printing.

## Notes

- Always run `autoCutout` while on the original image layer so the AI can detect the subject.
- The selection persists when creating a new layer, allowing you to fill on the new layer.
- For better edge quality, consider using cloud processing: add `"imageProcessingSelectSubjectPrefs": { "_enum": "imageProcessingSelectSubjectPrefs", "_value": "imageProcessingModeCloud" }` to the `autoCutout` action.
- The resulting mask layer can be renamed using the [Rename Layer](../layer_management/rename_layer.md) action.

