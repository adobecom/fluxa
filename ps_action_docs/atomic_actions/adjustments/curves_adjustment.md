# Configure/Apply Curves Adjustment

**Action:** `set` or `curves`
**Target:** `adjustmentLayer` or active layer

Sets the curve points for specific channels. This can be done by configuring an existing adjustment layer (`set`), creating a new adjustment layer (`make`), or applying it destructively to the active layer (`curves`).

> **Note:** The `curves` object structure defined here is used in three contexts:
> 1.  **Modifying (`set`):** To update an existing adjustment layer.
> 2.  **Creating (`make`):** As the `using` object when creating a new adjustment layer.
> 3.  **Applying (`curves`):** Directly applying the adjustment to the active layer (destructive).

## JSON Structure

### 1. Modifying an Adjustment Layer (`set`)

**Basic Example:**

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

### 2. Complex Multi-Channel Example (`set`)

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

### 3. Applying Destructively (`curves`)

Directly applies the curves adjustment to the current layer.

```json
{
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
```

## Parameters

- `adjustment`: Array of channel configurations.
- `channel._value`: Target channel.
    - `composite`: The main RGB channel.
    - `red`: Red channel.
    - `grain`: Green channel (internal name is 'grain').
    - `blue`: Blue channel.
- `curve`: Array of points defining the curve.
    - `horizontal`: Input level (0-255) - X axis.
    - `vertical`: Output level (0-255) - Y axis.
