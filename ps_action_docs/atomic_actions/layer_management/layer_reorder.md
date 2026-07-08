# Layer Reordering

**Action:** `move`  
**Target:** Layer(s) to move  
**Menu Location:** Layer > Arrange > Bring to Front / Bring Forward / Send Backward / Send to Back

Reorders layers in the layer stack by moving them to specific positions or relative to other layers. This is essential for creating layer "sandwich" effects and controlling the visual stacking order of layers.

## Move Layer to Specific Index

Moves the selected layer(s) to a specific index position in the layer stack.

```json
{
    "_obj": "move",
    "_target": [
        {
            "_enum": "ordinal",
            "_ref": "layer",
            "_value": "targetEnum"
        }
    ],
    "to": {
        "_ref": "layer",
        "_index": 2
    },
    "version": 5,
    "adjustment": true
}
```

## Bring Layer to Front

Moves the selected layer to the top of the layer stack (front).

```json
{
    "_obj": "move",
    "_target": [
        {
            "_enum": "ordinal",
            "_ref": "layer",
            "_value": "targetEnum"
        }
    ],
    "to": {
        "_enum": "ordinal",
        "_ref": "layer",
        "_value": "front"
    }
}
```

## Send Layer to Back

Moves the selected layer to the bottom of the layer stack (back), above the background layer if present.

```json
{
    "_obj": "move",
    "_target": [
        {
            "_enum": "ordinal",
            "_ref": "layer",
            "_value": "targetEnum"
        }
    ],
    "to": {
        "_enum": "ordinal",
        "_ref": "layer",
        "_value": "back"
    }
}
```

## Bring Layer Forward (One Position)

Moves the selected layer up one position in the stack.

```json
{
    "_obj": "move",
    "_target": [
        {
            "_enum": "ordinal",
            "_ref": "layer",
            "_value": "targetEnum"
        }
    ],
    "to": {
        "_enum": "ordinal",
        "_ref": "layer",
        "_value": "next"
    }
}
```

## Send Layer Backward (One Position)

Moves the selected layer down one position in the stack.

```json
{
    "_obj": "move",
    "_target": [
        {
            "_enum": "ordinal",
            "_ref": "layer",
            "_value": "targetEnum"
        }
    ],
    "to": {
        "_enum": "ordinal",
        "_ref": "layer",
        "_value": "previous"
    }
}
```

## Move Layer Above Another Layer

Moves a specific layer above another layer by targeting both layers.

```json
{
    "_obj": "move",
    "_target": [
        {
            "_ref": "layer",
            "_index": 3
        }
    ],
    "to": {
        "_ref": "layer",
        "_index": 1
    },
    "version": 5,
    "adjustment": true
}
```

## Move Multiple Layers

Moves multiple selected layers together to a new position.

```json
{
    "_obj": "move",
    "_target": [
        {
            "_ref": "layer",
            "_index": 2
        },
        {
            "_ref": "layer",
            "_index": 3
        }
    ],
    "to": {
        "_ref": "layer",
        "_index": 0
    },
    "version": 5,
    "adjustment": true
}
```

## Parameters

### Main Structure

-   `_obj`: `"move"` - Action type for moving/reordering layers
-   `_target`: Array containing one or more layer references to move
-   `to`: Reference object specifying the destination position
-   `version`: Integer (optional, default: 5) - Version of the move action
-   `adjustment`: Boolean (optional, default: `true`) - If true, arrangement behaves the same for group layers as PS6-PS8

### Target Layer Reference (`_target` array)

Each element can be:
-   `_enum`: `"ordinal"` with `_value`: `"targetEnum"` - Currently selected layer
-   `_ref`: `"layer"` with `_index`: Integer - Layer by index
-   `_ref`: `"layer"` with `_id`: Integer - Layer by unique ID
-   `_ref`: `"layer"` with `_name`: String - Layer by name

### Destination Reference (`to` object)

Two methods for specifying destination:

**Method 1: Index-based positioning**
-   `_ref`: `"layer"`
-   `_index`: Integer - Target index position (0-based, where 0 is the top)

**Method 2: Ordinal-based positioning**
-   `_enum`: `"ordinal"`
-   `_ref`: `"layer"`
-   `_value`: One of:
    -   `"front"` - Move to the top of the stack
    -   `"back"` - Move to the bottom (above background layer)
    -   `"next"` or `"forward"` - Move up one position
    -   `"previous"` or `"backward"` - Move down one position

## Notes

- Layer indices are 0-based, where 0 represents the topmost layer in the stack.
- The background layer (if present) is always at the bottom and cannot be moved above other layers.
- When moving layers within groups, the indices are relative to the group's layer stack.
- Multiple layers can be moved together by including multiple references in the `_target` array.
- The `adjustment` parameter affects how group layers are handled during the move operation.
- Ordinal values (`front`, `back`, `next`, `previous`) provide relative positioning and are useful when you don't know the exact index.
- Index-based moves are more precise and useful when you know the exact target position.
- Moving a layer above itself or to its current position is a no-op and will not cause an error.
- Layer reordering affects the visual stacking order and can impact how layers blend and interact with each other.

