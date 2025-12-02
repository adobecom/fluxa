# Agent-Based Photoshop Action Generator - Implementation Plan

## Overview

Replace hardcoded prompts in `photoshop_actions.py` with a DeepAgents-based implementation that dynamically reads documentation from `ps_action_docs/atomic_actions/` folder.

## Current System Flow

```
run.sh → fluxa CLI → youtube_extractor → PhotoshopActionGenerator → ActionJSON
                                              ↓
                                    photoshop_actions.py (600+ lines hardcoded prompts)
```

## New Agent System Flow

```
run.sh --use-agent → fluxa CLI → youtube_extractor → AgentPhotoshopActionGenerator → ActionJSON
                                                              ↓
                                                    DeepAgents with FilesystemBackend
                                                              ↓
                                                    Reads ps_action_docs/atomic_actions/*.md dynamically
```

## Key Components

### 1. DeepAgents Configuration
- **Library**: `deepagents` (https://github.com/langchain-ai/deepagents)
- **Model**: GPT-4o (same as current system)
- **Backend**: `FilesystemBackend` with root at project directory
- **Tools**: Built-in filesystem tools (`ls`, `read_file`, `grep`, `glob`)

### 2. Documentation Structure
```
ps_action_docs/atomic_actions/
├── adjustments/
│   ├── black_and_white.md
│   ├── brightness_contrast.md
│   ├── create_adjustment_layer.md
│   ├── curves_adjustment.md
│   ├── desaturate.md
│   ├── levels_adjustment.md
│   └── photo_filter.md
├── channels/
│   └── select_channel.md
├── filters/
│   ├── add_noise.md
│   ├── camera_raw_filter.md
│   ├── difference_clouds.md
│   ├── displace.md
│   ├── gaussian_blur.md
│   ├── motion_blur.md
│   └── unsharp_mask.md
├── image/
│   └── crop.md
├── layer_management/
│   ├── convert_to_smart_object.md
│   ├── create_clipping_mask.md
│   ├── create_group.md
│   ├── create_mask.md
│   ├── create_new_layer.md
│   ├── delete_layer.md
│   ├── duplicate_layer.md
│   ├── fill_opacity.md
│   ├── fill.md
│   ├── hide_layer.md
│   ├── layer_reorder.md
│   ├── link_layers.md
│   ├── merge_layers.md
│   ├── rename_layer.md
│   ├── select_layer.md
│   ├── set_layer_properties.md
│   ├── set_opacity.md
│   ├── stroke_layer_style.md
│   └── transform.md
├── selection/
│   ├── color_range.md
│   ├── select_subject.md
│   └── subject_mask.md
└── text_layer.md
```

## Files to Create/Modify

### New Files
1. `actionJSON-generator/src/fluxa/generators/agent_photoshop_action_generator.py`
   - New `AgentPhotoshopActionGenerator` class using DeepAgents

### Modified Files
1. `actionJSON-generator/src/fluxa/cli.py`
   - Add `--use-agent` flag
   - Conditionally use agent-based generator

2. `actionJSON-generator/requirements.txt`
   - Add `deepagents` dependency

3. `run.sh`
   - Add `--use-agent` flag support

## Implementation Details

### AgentPhotoshopActionGenerator Class

```python
class AgentPhotoshopActionGenerator:
    """Generate Photoshop API JSON using DeepAgents with dynamic documentation reading"""
    
    def __init__(self, api_key: str, model: str = "gpt-5.1", docs_path: str = None):
        # Configure DeepAgents with FilesystemBackend
        # Set up agent with custom system prompt
        pass
    
    def generate(self, content: str, source: str, source_type: str) -> Dict[str, Any]:
        # Invoke agent with transcript
        # Agent reads docs dynamically
        # Returns ActionJSON array
        pass
```

### Agent System Prompt Strategy

The system prompt will instruct the agent to:
1. Analyze the tutorial transcript for Photoshop operations
2. Use filesystem tools to search documentation
3. Read relevant .md files to understand operation formats
4. Map transcript steps to ActionJSON operations
5. Output valid JSON array

### Agent Workflow

1. **Input**: Tutorial transcript
2. **Step 1**: Agent uses `ls` to explore `ps_action_docs/atomic_actions/`
3. **Step 2**: Agent uses `grep` to find relevant docs based on keywords
4. **Step 3**: Agent uses `read_file` to read specific operation docs
5. **Step 4**: Agent maps transcript steps to operations using doc formats
6. **Step 5**: Agent outputs JSON array

## Error Handling

- If agent cannot find matching operations: Raise `ValueError` with descriptive message
- Log all agent tool calls for debugging
- Validate output JSON format before returning

## Testing Strategy

1. Start with known implementable action (e.g., brightness/contrast adjustment)
2. Run with `--use-agent` flag
3. Compare output with current system output
4. Iterate based on logs

## Dependencies

```
deepagents>=0.2.8
langchain>=0.1.0
langchain-openai>=0.0.5
```

## CLI Changes

```bash
# Current usage
fluxa https://youtube.com/... -o output.json

# New usage with agent
fluxa https://youtube.com/... -o output.json --use-agent
```

## run.sh Changes

```bash
# Add flag handling
USE_AGENT=${3:-false}

if [ "$USE_AGENT" = "--use-agent" ]; then
    fluxa $TUTORIAL_LINK -o output.json --use-agent
else
    fluxa $TUTORIAL_LINK -o output.json
fi
```

## Success Criteria

1. Agent successfully reads documentation files
2. Agent maps transcript steps to correct operations
3. Output JSON is valid and matches expected format
4. Same interface as existing generator (drop-in replacement)

