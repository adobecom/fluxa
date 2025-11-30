# Configure/Apply Photo Filter Adjustment

**Action:** `make` or `set`  
**Target:** `adjustmentLayer`

Creates a new Photo Filter adjustment layer or modifies an existing one. This filter simulates looking through a colored filter, warming or cooling the image.

## JSON Structure

### 1. Creating a Photo Filter Layer (`make`)

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
            "_obj": "photoFilter",
            "color": {
                "_obj": "labColor",
                "a": 32.0,
                "b": 120.0,
                "luminance": 67.06
            },
            "density": 25,
            "preserveLuminosity": true
        }
    }
}
```

### 2. Modifying Existing Photo Filter (`set`)

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
        "_obj": "photoFilter",
        "color": {
            "_obj": "HSBColorClass",
            "brightness": 100.0,
            "hue": {
                "_unit": "angleUnit",
                "_value": 35.0
            },
            "saturation": 32.0
        },
        "density": 59,
        "preserveLuminosity": true
    }
}
```

## Parameters

- `type._obj` / `to._obj`: Must be `photoFilter`.
- `color`: Defines the filter color. Can use different color models:
    - **Lab Color** (`labColor`): `luminance`, `a`, `b`.
    - **HSB Color** (`HSBColorClass`): `hue` (angle), `saturation`, `brightness`.
    - **RGB Color** (`RGBColor`): `red`, `green`, `blue` (common standard, though not shown in this specific example).
- `density`: Integer (0-100). Controls the intensity of the filter.
- `preserveLuminosity`: Boolean. If `true`, maintains the image's brightness values while tinting.

