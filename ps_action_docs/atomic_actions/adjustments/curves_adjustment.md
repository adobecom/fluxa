# Configure Curves Adjustment

**Action:** `set`  
**Target:** `adjustmentLayer` (current) -> `curves`

Sets the curve points for specific channels in a Curves adjustment layer. This action supports complex color grading by defining independent curves for the Composite (RGB), Red, Green (Grain), and Blue channels.

> **Note:** The `curves` object structure defined here can be used in two contexts:
> 1.  **Modifying (`set`):** As shown in the examples below, to update an existing layer.
> 2.  **Creating (`make`):** As the `using.type` object when creating a new adjustment layer (see `create_adjustment_layer.md`).

## JSON Structure

### Basic Example
A simple S-curve for contrast.

```json
{
    "_obj": "set",
    "_target": [
        {
            "_enum": "ordinal",
            "_ref": "adjustmentLayer",
            "_value": "targetEnum"
        }
    ],
    "to": {
        "_obj": "curves",
        "adjustment": [
            {
                "_obj": "curvesAdjustment",
                "channel": {
                    "_enum": "channel",
                    "_ref": "channel",
                    "_value": "composite" 
                },
                "curve": [
                    { "_obj": "paint", "horizontal": 0.0, "vertical": 0.0 },
                    { "_obj": "paint", "horizontal": 255.0, "vertical": 255.0 }
                ]
            }
        ],
        "presetKind": {
            "_enum": "presetKindType",
            "_value": "presetKindCustom"
        }
    }
}
```

### Complex Multi-Channel Example
This example demonstrates a "Color Pop" style adjustment. It uses multiple points to create a matte look (lifting blacks) on the composite channel, and adjusts individual color channels to warm the image.

**Key Notes:**
*   **Multiple Objects:** The `adjustment` array contains one object per channel.
*   **Channel Names:** Green is referred to as `grain`.
*   **Curve Points:** You can add as many points as needed (`horizontal` = Input, `vertical` = Output) to define complex shapes.

```json
{
    "_obj": "set",
    "_target": [
        {
            "_enum": "ordinal",
            "_ref": "adjustmentLayer",
            "_value": "targetEnum"
        }
    ],
    "to": {
        "_obj": "curves",
        "adjustment": [
            {
                // 1. Composite (RGB) Channel: Matte S-Curve
                "_obj": "curvesAdjustment",
                "channel": { "_enum": "channel", "_ref": "channel", "_value": "composite" },
                "curve": [
                    { "_obj": "paint", "horizontal": 0.0, "vertical": 16.0 },   // Lift blacks
                    { "_obj": "paint", "horizontal": 70.0, "vertical": 55.0 },  // Shadow contrast
                    { "_obj": "paint", "horizontal": 128.0, "vertical": 128.0 },// Midtone anchor
                    { "_obj": "paint", "horizontal": 255.0, "vertical": 245.0 } // Crush whites
                ]
            },
            {
                // 2. Red Channel: Slight boost in midtones
                "_obj": "curvesAdjustment",
                "channel": { "_enum": "channel", "_ref": "channel", "_value": "red" },
                "curve": [
                    { "_obj": "paint", "horizontal": 0.0, "vertical": 0.0 },
                    { "_obj": "paint", "horizontal": 128.0, "vertical": 135.0 },
                    { "_obj": "paint", "horizontal": 255.0, "vertical": 255.0 }
                ]
            },
            {
                // 3. Green (Grain) Channel
                "_obj": "curvesAdjustment",
                "channel": { "_enum": "channel", "_ref": "channel", "_value": "grain" },
                "curve": [
                    { "_obj": "paint", "horizontal": 0.0, "vertical": 0.0 },
                    { "_obj": "paint", "horizontal": 128.0, "vertical": 130.0 },
                    { "_obj": "paint", "horizontal": 255.0, "vertical": 255.0 }
                ]
            },
            {
                // 4. Blue Channel: Slight reduction (warms the image)
                "_obj": "curvesAdjustment",
                "channel": { "_enum": "channel", "_ref": "channel", "_value": "blue" },
                "curve": [
                    { "_obj": "paint", "horizontal": 0.0, "vertical": 0.0 },
                    { "_obj": "paint", "horizontal": 128.0, "vertical": 120.0 },
                    { "_obj": "paint", "horizontal": 255.0, "vertical": 255.0 }
                ]
            }
        ],
        "presetKind": {
            "_enum": "presetKindType",
            "_value": "presetKindCustom"
        }
    }
}
```

## Parameters

- `to.adjustment`: Array of channel configurations.
- `channel._value`: Target channel.
    - `composite`: The main RGB channel.
    - `red`: Red channel.
    - `grain`: Green channel (internal name is 'grain').
    - `blue`: Blue channel.
- `curve`: Array of points defining the curve.
    - `horizontal`: Input level (0-255) - X axis.
    - `vertical`: Output level (0-255) - Y axis.
