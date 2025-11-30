# Adobe Camera Raw Filter

**Action:** `Adobe Camera Raw Filter`  
**Target:** None (Applied to current layer)

Applies the Adobe Camera Raw Filter, which allows for powerful color correction and enhancements similar to Lightroom.

## JSON Structure

The Camera Raw Filter object is extensive. Below are the key parameters for common adjustments.

```json
{
    "_obj": "Adobe Camera Raw Filter",
    "$Temp": 10,          // Temperature (Blue-Yellow)
    "$Tint": 0,           // Tint (Green-Magenta)
    "$Ex12": 0.50,        // Exposure
    "$Cr12": 10,          // Contrast
    "$Hi12": -20,         // Highlights
    "$Sh12": 20,          // Shadows
    "$Wh12": 10,          // Whites
    "$Bk12": -10,         // Blacks
    "$Cl12": 15,          // Clarity
    "$Vibr": 20,          // Vibrance
    "$Sat": 0,            // Saturation
    "$CrvB": [0, 0, 255, 255], // Blue Channel Curve [in, out, in, out...]
    "$CrvG": [0, 0, 255, 255], // Green Channel Curve
    "$CrvR": [0, 0, 255, 255], // Red Channel Curve
    "$Crv":  [0, 0, 255, 255], // Composite Curve (sometimes $Crv, sometimes implied)
    "sharpen": 25
}
```

## Key Parameters

### Basic Tone
- `$Temp`: Temperature (-100 to 100). Negative = Blue, Positive = Yellow.
- `$Tint`: Tint (-100 to 100). Negative = Green, Positive = Magenta.
- `$Ex12`: Exposure (-5.00 to +5.00).
- `$Cr12`: Contrast (-100 to 100).
- `$Hi12`: Highlights (-100 to 100).
- `$Sh12`: Shadows (-100 to 100).
- `$Wh12`: Whites (-100 to 100).
- `$Bk12`: Blacks (-100 to 100).

### Texture & Presence
- `$Cl12`: Clarity (-100 to 100).
- `$Vibr`: Vibrance (-100 to 100).
- `$Sat`: Saturation (-100 to 100).
- `$Dhze`: Dehaze (-100 to 100).

### Curves
Curves are represented as flat arrays of integers `[in1, out1, in2, out2, ...]`.
- `$CrvR`: Red Channel Curve.
- `$CrvG`: Green Channel Curve.
- `$CrvB`: Blue Channel Curve.

### Detail
- `sharpen`: Sharpening amount (0-150).

### Other
- `$CMod`: Process Version (e.g., "Filter").
- `$CamP`: Profile (e.g., "Embedded").

## Example from 'Chogolate' Effect

```json
{
    "_obj": "Adobe Camera Raw Filter",
    "$Temp": -8,
    "$Tint": 4,
    "$Ex12": 0.0,
    "$Cr12": 9,
    "$Hi12": -13,
    "$Sh12": 18,
    "$Wh12": 10,
    "$Bk12": -3,
    "$Cl12": 6,
    "$Vibr": -11,
    "$CrvR": [0, 0, 255, 255],
    "$CrvG": [0, 0, 255, 255],
    "$CrvB": [0, 0, 255, 255],
    "sharpen": 0
}
```

