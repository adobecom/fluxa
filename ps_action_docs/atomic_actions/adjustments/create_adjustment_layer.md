# Create Adjustment Layer

**Action:** `make`  
**Target:** `adjustmentLayer`

Creates a new adjustment layer (e.g., Curves, Levels, Hue/Saturation).

## JSON Structure

```json
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
            "_obj": "curves", 
            "presetKind": {
                "_enum": "presetKindType",
                "_value": "presetKindDefault"
            }
        }
    }
}
```

### Example: Create with Custom Settings
You can also define the adjustment settings (like curve points) directly within the `make` action.

```json
{
  "_obj": "make",
  "_target": [{ "_ref": "adjustmentLayer" }],
  "using": {
    "_obj": "adjustmentLayer",
    "type": {
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
            { "_obj": "paint", "horizontal": 128.0, "vertical": 128.0 },
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
}
```

## Parameters

- `using.type._obj`: The type of adjustment layer (e.g., `curves`, `levels`, `brightnessContrast`).
- `using.type`: Can contain the full configuration object for the adjustment (matches the structure used in `set` actions for that adjustment type).

