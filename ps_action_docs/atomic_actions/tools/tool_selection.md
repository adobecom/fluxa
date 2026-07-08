# Tool Selection

**Action:** `select`  
**Target:** Tool reference  
**Menu Location:** Tools panel or keyboard shortcuts

Selects a tool from the Photoshop toolbar. Tools can be selected by their tool name reference, which corresponds to keyboard shortcuts (e.g., "G" for Gradient tool, "V" for Move tool).

## Select Gradient Tool

Selects the Gradient tool (keyboard shortcut: G).

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

## Select Move Tool

Selects the Move tool (keyboard shortcut: V).

```json
{
    "_obj": "select",
    "_target": [
        {
            "_ref": "moveTool"
        }
    ]
}
```

## Select Brush Tool

Selects the Brush tool (keyboard shortcut: B).

```json
{
    "_obj": "select",
    "_target": [
        {
            "_ref": "paintbrushTool"
        }
    ]
}
```

## Select Text Tool

Selects the Type tool (keyboard shortcut: T).

```json
{
    "_obj": "select",
    "_target": [
        {
            "_ref": "typeCreateOrEditTool"
        }
    ]
}
```

## Select Crop Tool

Selects the Crop tool (keyboard shortcut: C).

```json
{
    "_obj": "select",
    "_target": [
        {
            "_ref": "cropTool"
        }
    ]
}
```

## Parameters

### Main Structure

-   `_obj`: `"select"` - Action type for selecting a tool
-   `_target`: Array containing a tool reference
    -   `_ref`: String - Tool name (see Tool Reference Names below)

## Tool Reference Names and Keyboard Shortcuts

### Selection Tools

| Tool Name | Reference Name | Keyboard Shortcut |
|-----------|----------------|-------------------|
| Move Tool | `moveTool` | V |
| Artboard Tool | `artboardTool` | V |
| Rectangular Marquee | `marqueeRectTool` | M |
| Elliptical Marquee | `marqueeEllipTool` | M |
| Single Row Marquee | `marqueeSingleRowTool` | - |
| Single Column Marquee | `marqueeSingleColumnTool` | - |
| Lasso Tool | `lassoTool` | L |
| Polygonal Lasso | `polySelTool` | L |
| Magnetic Lasso | `magneticLassoTool` | L |
| Quick Selection | `quickSelectTool` | W |
| Magic Wand | `magicWandTool` | W |
| Object Selection (Magic Lasso) | `magicLassoTool` | W |
| Selection Brush | `selectionLabSmartBrushTool` | W |

### Painting Tools

| Tool Name | Reference Name | Keyboard Shortcut |
|-----------|----------------|-------------------|
| Brush Tool | `paintbrushTool` | B |
| Pencil Tool | `pencilTool` | B |
| Color Replacement Brush | `colorReplacementBrushTool` | B |
| Mixer Brush | `wetBrushTool` | B |
| Eraser Tool | `eraserTool` | E |
| Background Eraser | `backgroundEraserTool` | E |
| Magic Eraser | `magicEraserTool` | E |
| Paint Bucket | `bucketTool` | G |
| Gradient Tool | `gradientTool` | G |

### Retouching Tools

| Tool Name | Reference Name | Keyboard Shortcut |
|-----------|----------------|-------------------|
| Spot Healing Brush | `spotHealingBrushTool` | J |
| Healing Brush | `magicStampTool` | J |
| Patch Tool | `patchSelection` | J |
| Content-Aware Move | `recomposeSelection` | J |
| Remove Tool | `removeTool` | J |
| Clone Stamp | `cloneStampTool` | S |
| Pattern Stamp | `patternStampTool` | S |
| History Brush | `historyBrushTool` | Y |
| Art History Brush | `artBrushTool` | Y |

### Adjustment Tools

| Tool Name | Reference Name | Keyboard Shortcut |
|-----------|----------------|-------------------|
| Dodge Tool | `dodgeTool` | O |
| Burn Tool | `burnInTool` | O |
| Sponge Tool | `saturationTool` | O |
| Blur Tool | `blurTool` | - |
| Sharpen Tool | `sharpenTool` | - |
| Smudge Tool | `smudgeTool` | - |

### Drawing Tools

| Tool Name | Reference Name | Keyboard Shortcut |
|-----------|----------------|-------------------|
| Pen Tool | `penTool` | P |
| Freeform Pen | `freeformPenTool` | P |
| Curvature Pen | `curvaturePenTool` | P |
| Add Anchor Point | `addKnotTool` | - |
| Delete Anchor Point | `deleteKnotTool` | - |
| Convert Point | `convertKnotTool` | - |
| Direct Selection | `directSelectTool` | A |
| Path Selection | `pathComponentSelectTool` | A |

### Shape Tools

| Tool Name | Reference Name | Keyboard Shortcut |
|-----------|----------------|-------------------|
| Rectangle Tool | `rectangleTool` | U |
| Rounded Rectangle | `roundedRectangleTool` | U |
| Ellipse Tool | `ellipseTool` | U |
| Triangle Tool | `triangleTool` | U |
| Polygon Tool | `polygonTool` | U |
| Line Tool | `lineTool` | U |
| Custom Shape | `customShapeTool` | U |
| Frame Tool | `framedGroupTool` | K |

### Type Tools

| Tool Name | Reference Name | Keyboard Shortcut |
|-----------|----------------|-------------------|
| Horizontal Type | `typeCreateOrEditTool` | T |
| Vertical Type | `typeVerticalCreateOrEditTool` | T |
| Horizontal Type Mask | `typeCreateMaskTool` | T |
| Vertical Type Mask | `typeVerticalCreateMaskTool` | T |

### Navigation Tools

| Tool Name | Reference Name | Keyboard Shortcut |
|-----------|----------------|-------------------|
| Hand Tool | `handTool` | H |
| Rotate View | `rotateTool` | H |
| Zoom Tool | `zoomTool` | Z |

### Measurement Tools

| Tool Name | Reference Name | Keyboard Shortcut |
|-----------|----------------|-------------------|
| Eyedropper Tool | `eyedropperTool` | I |
| Color Sampler | `colorSamplerTool` | I |
| Ruler Tool | `rulerTool` | I |
| Note Tool | `textAnnotTool` | I |
| Count Tool | `countTool` | - |

### Other Tools

| Tool Name | Reference Name | Keyboard Shortcut |
|-----------|----------------|-------------------|
| Crop Tool | `cropTool` | C |
| Perspective Crop | `perspectiveCropTool` | C |
| Slice Tool | `sliceTool` | C |
| Slice Select | `sliceSelectTool` | C |
| Place Tool | `placeTool` | - |
| Transform | `transformTool` | - |
| Red Eye | `redEyeTool` | - |
| Adjustment Brush | `adjustmentBrushTool` | - |

### Selection Lab Tools

| Tool Name | Reference Name | Keyboard Shortcut |
|-----------|----------------|-------------------|
| Select Mask Quick Select | `selectionLabSmartBrushTool` | - |
| Select Mask Refine Edge | `selectionLabRefineTool` | - |
| Select Mask Brush | `selectionLabDumbBrushTool` | - |
| Select Mask Auto Masking | `selectionLabMagicLassoTool` | - |
| Select Mask Lasso | `selectionLabLassoTool` | - |

## Notes

- Tool selection uses the `select` action with a tool reference in the `_target` array.
- The tool reference uses `_ref` with the tool name string (e.g., `"gradientTool"`, `"moveTool"`).
- Keyboard shortcuts are case-insensitive - pressing "G" or "g" will select the Gradient tool.
- Some tools share keyboard shortcuts and cycle through related tools (e.g., M cycles through Marquee tools, L cycles through Lasso tools).
- Holding Shift while pressing a tool shortcut often cycles to the alternate tool in a tool group.
- Tool selection is immediate - the tool becomes active as soon as the action is executed.
- Some tools may require a document to be open before they can be selected.
- Tool selection does not require any additional parameters beyond the tool reference.
- The tool name strings are consistent across different Photoshop versions, but new tools may be added in future versions.
- Some tools may not be available in all Photoshop editions or configurations.
- Tool selection can be combined with other actions in a batchPlay array for complex workflows.

