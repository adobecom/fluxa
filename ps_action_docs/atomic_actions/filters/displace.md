# Displace Filter

**Action:** `displace`  
**Target:** Active layer  
**Menu Location:** Filter > Distort > Displace

Distorts/warps the active layer based on a displacement map image. The displacement map is a grayscale image where:
- **50% gray (128)** = No displacement
- **Lighter values** = Shift pixels in positive direction
- **Darker values** = Shift pixels in negative direction

This filter is commonly used to wrap text or textures around 3D surfaces, facial contours, or fabric folds.

## Apply Displace Filter

Applies the Displace filter to the currently selected layer.

```json
{
    "_obj": "displace",
    "horizontalScale": 10,
    "verticalScale": 10,
    "displacementMap": {
        "_enum": "displacementMap",
        "_value": "stretchToFit"
    },
    "undefinedArea": {
        "_enum": "undefinedArea",
        "_value": "repeatEdgePixels"
    },
    "displaceFile": {
        "_kind": "local",
        "_path": "/path/to/displacement_map.psd"
    }
}
```

## Example with Tile Displacement

Applies Displace filter with tiled displacement map and wrap-around for undefined areas.

```json
{
    "_obj": "displace",
    "horizontalScale": 15,
    "verticalScale": 20,
    "displacementMap": {
        "_enum": "displacementMap",
        "_value": "tile"
    },
    "undefinedArea": {
        "_enum": "undefinedArea",
        "_value": "wrapAround"
    },
    "displaceFile": {
        "_kind": "local",
        "_path": "/path/to/tile_pattern.psd"
    }
}
```

## Parameters

-   `horizontalScale`: Integer value (typically -999 to 999) controlling the amount of horizontal distortion. Positive values shift pixels right, negative values shift left.
-   `verticalScale`: Integer value (typically -999 to 999) controlling the amount of vertical distortion. Positive values shift pixels down, negative values shift up.
-   `displacementMap`: Enum object specifying how the displacement map is applied to the image.
    -   `_enum`: `"displacementMap"`
    -   `_value`: Either `"stretchToFit"` or `"tile"`
        -   `"stretchToFit"`: Stretches the displacement map to fit the image dimensions
        -   `"tile"`: Tiles the displacement map across the image
-   `undefinedArea`: Enum object specifying how areas outside the displacement map boundaries are handled.
    -   `_enum`: `"undefinedArea"`
    -   `_value`: Either `"repeatEdgePixels"` or `"wrapAround"`
        -   `"repeatEdgePixels"`: Repeats the edge pixels of the displacement map
        -   `"wrapAround"`: Wraps the displacement map around (tiles it)
-   `displaceFile`: Object specifying the path to the displacement map file.
    -   `_kind`: `"local"` (indicates a local file path)
    -   `_path`: String path to the displacement map image file (typically a PSD file)

## Use Case: Text Portrait Effect

In the Text Portrait effect, this filter warps text around facial contours:
1. Create a blurred grayscale version of the face → save as PSD
2. Apply Displace filter to the text layer
3. Reference the saved PSD as the displacement map
4. The text will warp to follow the face's light/dark contours

## Related Actions

- `gaussianBlur` - Soften the displacement map for smoother warping
- `mergeVisible` - Create the displacement map from visible layers
- Black & White adjustment - Convert face to grayscale for the map

## Notes

- The displacement map should be a grayscale image (or Photoshop will use the first channel).
- The filter reads the displacement map's luminance values to determine pixel shifts.
- Higher scale values create more dramatic distortion effects.
- The displacement map file path must be accessible and valid for the filter to work correctly.

