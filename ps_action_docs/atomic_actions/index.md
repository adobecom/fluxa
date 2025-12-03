# Photoshop ActionJSON - Atomic Actions Index

This index lists all available atomic actions for generating Photoshop ActionJSON. Use the file paths below to read detailed documentation for each operation.

## Adjustments (`adjustments/`)

| File | Description |
|------|-------------|
| `adjustments/black_and_white.md` | Convert image to black and white with channel mixing |
| `adjustments/brightness_contrast.md` | Adjust brightness and contrast levels |
| `adjustments/create_adjustment_layer.md` | Create non-destructive adjustment layers |
| `adjustments/curves_adjustment.md` | Fine-tune tonal range with curves |
| `adjustments/desaturate.md` | Remove all color from a layer (grayscale) |
| `adjustments/levels_adjustment.md` | Adjust shadows, midtones, and highlights |
| `adjustments/photo_filter.md` | Apply color filter effects |

## Channels (`channels/`)

| File | Description |
|------|-------------|
| `channels/select_channel.md` | Select specific color channels (RGB, Red, Green, Blue) |

## Filters (`filters/`)

| File | Description |
|------|-------------|
| `filters/add_noise.md` | Add grain/noise to an image |
| `filters/camera_raw_filter.md` | Apply Camera Raw adjustments |
| `filters/difference_clouds.md` | Generate cloud-like patterns |
| `filters/displace.md` | Distort image using a displacement map |
| `filters/gaussian_blur.md` | Apply smooth blur effect |
| `filters/harmonize.md` | AI-powered color/lighting harmonization for compositing |
| `filters/smart_filters.md` | Apply non-destructive filters to smart objects |
| `filters/motion_blur.md` | Apply directional motion blur |
| `filters/oil_paint.md` | Apply oil painting artistic effect |
| `filters/unsharp_mask.md` | Sharpen image edges |

## Image (`image/`)

| File | Description |
|------|-------------|
| `image/crop.md` | Crop the canvas to specified dimensions |

## Layer Management (`layer_management/`)

| File | Description |
|------|-------------|
| `layer_management/convert_to_smart_object.md` | Convert layer(s) to smart object for non-destructive editing |
| `layer_management/create_clipping_mask.md` | Clip layer to the shape of layer below |
| `layer_management/create_group.md` | Create layer group/folder |
| `layer_management/create_mask.md` | Add layer mask from selection or transparency |
| `layer_management/create_new_layer.md` | Create a new empty layer |
| `layer_management/delete_layer.md` | Delete a layer |
| `layer_management/duplicate_layer.md` | Duplicate/copy a layer |
| `layer_management/fill_opacity.md` | Set fill opacity (affects content, not effects) |
| `layer_management/fill.md` | Fill layer/selection with color or pattern |
| `layer_management/hide_layer.md` | Show or hide a layer |
| `layer_management/layer_reorder.md` | Move layers up/down in stack (bring to front, send to back) |
| `layer_management/link_layers.md` | Link/unlink layers for synchronized transforms |
| `layer_management/merge_layers.md` | Merge multiple layers into one |
| `layer_management/place_image.md` | Place/import additional image (for multi-image compositing) |
| `layer_management/remove_background.md` | AI-powered background removal (creates mask hiding background) |
| `layer_management/rename_layer.md` | Rename a layer |
| `layer_management/select_layer.md` | Select/target a specific layer |
| `layer_management/set_layer_properties.md` | Set various layer properties |
| `layer_management/set_opacity.md` | Set layer opacity (affects content and effects) |
| `layer_management/stroke_layer_style.md` | Add stroke/outline layer effect |
| `layer_management/transform.md` | Scale, rotate, skew, or flip a layer |

## Selection (`selection/`)

| File | Description |
|------|-------------|
| `selection/color_range.md` | Select pixels by color similarity |
| `selection/deselect.md` | Clear selection (remove marching ants) - use after creating mask |
| `selection/select_subject.md` | AI-powered subject selection |
| `selection/subject_mask.md` | Create mask from subject selection |

## Text (`text_layer.md`)

| File | Description |
|------|-------------|
| `text_layer.md` | Create and style text layers |

## Tools (`tools/`)

| File | Description |
|------|-------------|
| `tools/tool_selection.md` | Select Photoshop tools (Gradient, Brush, Move, Type, etc.) |

---

## Quick Reference: Common Operations

| Operation | File to Read |
|-----------|--------------|
| Duplicate layer | `layer_management/duplicate_layer.md` |
| Select subject (AI) | `selection/select_subject.md` |
| Create layer mask | `layer_management/create_mask.md` |
| Deselect (clear selection) | `selection/deselect.md` |
| Add text | `text_layer.md` |
| Scale/transform | `layer_management/transform.md` |
| Convert to smart object | `layer_management/convert_to_smart_object.md` |
| Move layer order | `layer_management/layer_reorder.md` |
| Set fill to 0% | `layer_management/fill_opacity.md` |
| Add stroke effect | `layer_management/stroke_layer_style.md` |
| Create clipping mask | `layer_management/create_clipping_mask.md` |
| Link layers | `layer_management/link_layers.md` |
| Gaussian blur | `filters/gaussian_blur.md` |
| Desaturate | `adjustments/desaturate.md` |
| Invert colors | `adjustments/levels_adjustment.md` (use curves/levels for invert) |
| Select a tool (Gradient, Brush, etc.) | `tools/tool_selection.md` |
| Place/import second image | `layer_management/place_image.md` |
| Harmonize colors/lighting (AI) | `filters/harmonize.md` |
| Remove background (AI) | `layer_management/remove_background.md` |
<!-- doc -->


