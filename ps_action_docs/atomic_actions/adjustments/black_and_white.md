# Black & White Adjustment

**Action:** `make` or `set`  
**Target:** `adjustmentLayer`

Creates or modifies a Black & White adjustment layer, which converts color images to grayscale with control over how individual colors are converted.

## Create Black & White Layer

Creates a new adjustment layer with specific Black & White settings.

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
```

## Modify Existing Black & White Layer

Updates the settings of the currently selected Black & White adjustment layer.

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
        "_obj": "blackAndWhite",
        "red": 27,
        "yellow": 102,
        "grain": 21,
        "cyan": 33,
        "blue": 38,
        "magenta": 106,
        "useTint": true,
        "tintColor": {
            "_obj": "RGBColor",
            "red": 225.0,
            "grain": 211.0,
            "blue": 179.0
        }
    }
}
```

## Parameters

-   `red`, `yellow`, `cyan`, `blue`, `magenta`: Integer values (typically -200 to 300, default mix varies) controlling the gray contribution of each color channel.
-   `grain`: Controls the Green channel contribution (internal name is 'grain').
-   `useTint`: Boolean. If true, applies a color tint to the grayscale image.
-   `tintColor`: (Optional) Object defining the tint color if `useTint` is true.
    -   `_obj`: `RGBColor`
    -   `red`, `grain`, `blue`: Color values (0-255).

