# ColorPop Composite Action

**Action Name:** ColorPop  
**Description:** Enhances image vibrance and contrast using a specific Curves configuration and opacity layering.

This composite action is built from a sequence of [atomic actions](../atomic_actions/).

## Workflow Steps

### 1. Setup Layer Group
*   **Atomic Action:** [Create Group](../atomic_actions/layer_management/create_group.md)
*   **Details:** Creates a new group named "Group 1".

### 2. Rename Target Layer
*   **Atomic Action:** [Rename Layer](../atomic_actions/layer_management/rename_layer.md)
*   **Details:** Renames the active layer to "Fashion Colors POP".

### 3. Initialize Curves Adjustment
*   **Atomic Action:** [Create Adjustment Layer](../atomic_actions/adjustments/create_adjustment_layer.md)
*   **Details:** Adds a default Curves adjustment layer.

### 4. Apply Color Grading
*   **Atomic Action:** [Configure Curves](../atomic_actions/adjustments/curves_adjustment.md)
*   **Details:** Applies a custom S-curve to the composite channel and specific tints to Red, Green, and Blue channels to achieve the "pop" look.

### 5. Adjust Layer Opacity (Step 1)
*   **Atomic Action:** [Select Layer](../atomic_actions/layer_management/select_layer.md) -> [Set Opacity](../atomic_actions/layer_management/set_opacity.md)
*   **Details:** Selects the forward layer (likely the adjustment mask or layer itself) and sets opacity to **70%**.

### 6. Adjust Layer Opacity (Step 2)
*   **Atomic Action:** [Set Opacity](../atomic_actions/layer_management/set_opacity.md)
*   **Details:** Further adjusts opacity to **60%**.

### 7. Clean Up Selection
*   **Atomic Action:** [Select Layer](../atomic_actions/layer_management/select_layer.md) -> [Select Channel](../atomic_actions/channels/select_channel.md)
*   **Details:**
    1.  Selects the backward layer (navigates stack).
    2.  Resets channel selection to **RGB**.

### 8. Finalize Naming
*   **Atomic Action:** [Rename Layer](../atomic_actions/layer_management/rename_layer.md)
*   **Details:** Renames the final active layer to "Colors POP".

