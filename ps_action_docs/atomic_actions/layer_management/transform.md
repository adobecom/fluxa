# Transform Layer

**Action:** `transform`
**Target:** `layer`

Transforms the current layer (scale, rotate, etc.).

## JSON Structure

```json
{
    "_obj": "transform",
    "_target": [
        {
            "_enum": "ordinal",
            "_ref": "layer",
            "_value": "targetEnum"
        }
    ],
    "freeTransformCenterState": {
        "_enum": "quadCenterState",
        "_value": "QCSAverage"
    },
    "width": {
        "_unit": "percentUnit",
        "_value": 300.0
    },
    "height": {
        "_unit": "percentUnit",
        "_value": 300.0
    },
    "interfaceIconFrameDimmed": {
        "_enum": "interpolationType",
        "_value": "bicubic"
    },
    "linked": true,
    "offset": {
        "_obj": "offset",
        "horizontal": {
            "_unit": "distanceUnit",
            "_value": 0.0
        },
        "vertical": {
            "_unit": "distanceUnit",
            "_value": 0.0
        }
    }
}
```

## Parameters

- `width`: (Unit) Scaling width percentage.
- `height`: (Unit) Scaling height percentage.
- `offset`: (Object) Translation offset.
    - `horizontal`: distanceUnit value.
    - `vertical`: distanceUnit value.
- `interfaceIconFrameDimmed`: (Enum) Interpolation method.
    - `_value`: `bicubic`, `bilinear`, `nearestNeighbor`.
- `linked`: (Boolean) Whether width/height are linked.

