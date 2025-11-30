# Photoshop Action Documentation

This repository contains documentation for Photoshop Actions, organized into granular **Atomic Actions** (reusable building blocks) and **Composite Actions** (complete workflows).

## Architecture

The documentation is split to allow developers to understand the low-level JSON components and how they are assembled into complex effects.

### 📂 atomic_actions/
Contains the fundamental operations found in the Photoshop JSON schema.

*   **[layer_management/](atomic_actions/layer_management/)**: Actions for creating, grouping, renaming, and modifying basic layer properties (opacity, visibility).
*   **[adjustments/](atomic_actions/adjustments/)**: Actions specific to adjustment layers (Curves, Levels, etc.).
*   **[filters/](atomic_actions/filters/)**: Smart filters and destructive filter effects (Add Noise, Camera Raw, etc.).
*   **[channels/](atomic_actions/channels/)**: Actions for channel selection and manipulation.

### 📂 composite_actions/
Contains high-level workflows that combine atomic actions to achieve a specific visual effect.

*   **[ColorPop](composite_actions/color_pop.md)**: A color grading effect that utilizes groups, curves, and opacity adjustments.

## Usage

To create a new action:
1.  Identify the necessary steps from the `atomic_actions` library.
2.  Combine them in a JSON array sequence.
3.  Document the new workflow in `composite_actions/`.

